''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: ScriptClass.py
                    description: defines the parent class Script. This will get imported by each of the files in the run_scripts file. 
                    Allows the different scripts to define a subclass of Script, so they can inherit from this class but adjust the 
                    attributes and methods as needed. 

                    Imports all of the other components that are necessary for the running. i.e. the hardware stuff and the data analysis stuff. 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# Standard Library Imports 
import json
import time 
import csv
import sys 
from tabulate import tabulate
import threading 
from queue import Queue, Empty
import logging
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s',)
# logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')


# Third Party Imports
import pandas as pd 
from concurrent.futures import ThreadPoolExecutor
import RPi.GPIO as GPIO

# Local imports 
from class_definitions.Results import Results # manages output data 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.Pin import Pin # import pin class
from class_definitions.hardware_classes.pins_class.Lever import Lever # subclass to Pin
from class_definitions.hardware_classes.pins_class.Pellet import Pellet # subclass to Pin
from class_definitions.hardware_classes.Door import Door # built on top of multiple Pins

# Globals 
eventQ_lock = threading.Lock()


'''class SharedScript(): # objects that get shared among the script instances; This will only get created once, and then gets passed to Script instances  
    def __init__(self, pin_obj_dict=None, pin_values=None): 
         # Setup Dictionary of Names of Pins, and create the pin as a Pin Object or Lever Object (subclass of Pin)
        if pin_obj_dict is None: 
            self.pins = self.setup_pins_dict(pin_dict=None) # dictionary of all the individual pin objects
        else: 
            self.pins = pin_obj_dict # pins were already setup in previous script run
            
            
        # Thread Pool 
        self.executor = ThreadPoolExecutor(max_workers=20) 
        self.executor_manager = threading.Thread(target=self.monitor_for_future_results, daemon=True)
        self.futures = []
        self.stop_threads = False''' 
        
        
        

class Script(): # each script that runs gets its own instance of Script created 
    ''' 
        class Script: 
           meant for holding the information that all of the scripts have in common. 
           then, for each script, if it needs to add more it can override this parent class with a subclass 
    '''

    def __init__(self, csv_input, output_dir, key_values, pin_obj_dict=None, pin_values=None):

        # input and output files
        self.csv_input = csv_input
        self.output_dir = output_dir
        self.results = Results(csv_input, output_dir) # Resutls Class monitors output file tasks
        
        # Setup Values of user's Input Information for running Experiment
        self.key_values = self.change_key_values(key_values, csv_input['key_val_changes'])
        
        # Setup Dictionary of Names of Pins, and create the pin as a Pin Object or Lever Object (subclass of Pin)
        if pin_obj_dict is None: 
            self.pins = self.setup_pins_dict(pin_dict=None) # dictionary of all the individual pin objects
        else: 
            # pins were already setup in previous script run
            self.pins = pin_obj_dict # set to pin dict that is already setup 
            for pin in self.pins: 
                self.pins[pin].reset() # resets values
        
        # Group the pins up that are for controlling the doors, and pass to new Door object. 
        self.doors = self.setup_Doors() # returns dictionary for each door. 
        
        # Experiment Information 
        self.round = 0  
        self.start_time = time.time()
        
        # Thread Pool 
        self.executor = ThreadPoolExecutor(max_workers=20) 
        self.executor_manager = threading.Thread(target=self.monitor_for_future_results, daemon=True)
        self.futures = []
        self.stop_threads = False 
                    
    ''' ------------- Private Methods --------------------'''
    # Make changes to the key values if user added to column "key_val_changes" in csv file
    def change_key_values(self, key_values, key_val_changes): 
        if not (pd.isnull(key_val_changes)): # check if user wants to change any key values 
            key_val_changes_dict = json.loads(key_val_changes)
            for key in key_val_changes_dict: 
                if key in key_values: 
                    key_values.update({key: key_val_changes_dict.get(key)})
                else: 
                    print(f'** you asked to change the value of "{key}" which is not listed as a value that Magazine script needs to track, so skipped this one **')
            print("Here are your new key values: ", key_values)
        else: 
            print("No changes made to key values, just using the default key values:", key_values)
        return key_values

    
    ''' setup pins is to add individual Pin instances to a dictionary that can be accessed in ScriptClass '''                  
    def setup_pins_dict(self, pin_dict=None): 
        ''' called from ScriptClass.py during script setup. this returns the initalized pin_obj_dict which contains (pin_name->pin_class_instance) pairs '''
        # function accepts optional argument: user can choose to pass in their own pin dictionary, otherwise the default pins (defined in operant_cage_settings_default.py) are used 
        
        if (pin_dict==None): # check if user passed in argument. If not, assign pin_dict to the default values. 
            pin_dict = default_operant_settings.pins
        elif not pin_dict: # user passed argument, but the dictionary is empty.
            pin_dict = default_operant_settings.pins
        
        # create new dictionary where each element is (pin_name:Pin_class_instance)
        pin_obj_dict= {} # inialize empty dict
        
        # set the type of the pin based on the pin's name, and then create instance of Pin and append this to pin_obj_dict
        for key in pin_dict.keys(): 
            
            # instantiate pin object based on type
            
            if 'lever' in key: 
                pin_obj_dict[key] = Lever(key, pin_dict.get(key)) 
            elif 'pellet' in key: 
                pin_obj_dict[key] = Pellet(key, pin_dict.get(key))
            else: 
                pin_obj_dict[key] = Pin(key, pin_dict.get(key))
        
        return pin_obj_dict
        
        
    def setup_Doors(self):  # SJL: get pins of type door_1, then create a Door class for this door.

        door_dict = {}
        i = 1 
        pins_of_door_id = self.get_pins_of_type(f'door_{i}')
        while len(pins_of_door_id) != 0: # check if list is empty  
            
            # this assumes that the doors will be named in chronological order; door_1, door_2, door_3, etc. 
            # so, for example, if door_3 comes back with <None>, then we assume that we have only 2 doors 
            
            # create door_i instance and send the pins that belong to this door  
            door_dict[f'door_{i}'] = Door( f'door_{i}', pins_of_door_id)
            
            # increment and get next door 
            i = i + 1
            pins_of_door_id = self.get_pins_of_type(f'door_{i}')
        return door_dict
    

   
    ''' ------------- Public Methods ------------------------'''

    # # # # # # # # # # # # # # # # # # # # 
    #           Pin Functions             #
    # # # # # # # # # # # # # # # # # # # # 
    def get_pins_of_type(self, type): 
        # returns pins of the specified type 
        pin_dict = {}
        for p in self.pins: # loop thru the pins dictionary values which contains the Pin Object 
            # SJL: changed from if type==p to if type in p 
            if type in self.pins[p].name: # if pin's type matches the speicified type
                # print(f'{type} in {self.pins[p].name}')
                pin_dict[self.pins[p].name] = (self.pins[p]) # add pin object to dictionary
            else: pass # otherwise, go to next pin in the list 
        
        return pin_dict
    
    def print_pin_status(self):
    
        print("\033c", end="")
        sorted_pins = sorted(self.pins.keys())
        status = []
        num_pins = len(self.pins)
        for i in range(0,num_pins,2):
            
            if i+1<num_pins:
                status += [[sorted_pins[i], GPIO.input(self.pins[sorted_pins[i]].number),
                            sorted_pins[i+1], GPIO.input(self.pins[sorted_pins[i+1]].number)]]
            else:
                status += [[sorted_pins[i], GPIO.input(self.pins[sorted_pins[i]].number),
                            '', '']]
        print(tabulate(status, headers = ['pin', 'status', 'pin', 'status']))
        time.sleep(0.05)

        try:
            while True:
                self.print_pin_status()
                time.sleep(0.05)
        except KeyboardInterrupt:
            print('\n bye!')
            exit()
                
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #       Functions for managing/monitoring the Thread Pool and its resulting Futures                     #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def thread_pool_submit(self, event_name, func, *args, **kwargs): 
        future = self.executor.submit(func, *args, **kwargs)   
        self.futures.append([future, event_name]) # adds to list of futures to ensure it gets written to output once it finishes 

    def monitor_for_future_results(self): 
        # separate thread 
        while True: 
            ''' loop thru self.futures list(or queue?). Check if the future is done running. If it is, 
            then get its result and write them to event_queue. If it is not, then leave it be and go to the 
            next element. Repeat until the round has finished. 
            ''' 
            for future,name in (self.futures): 
                if future.done(): 
                    self.futures.remove([future,name]) # remove tuple at this index 
                    # self.futures.remove(future) # remove this future from the list
                    event_name, timestamp, ifEvent = future.result() # get result
                    print(f'Future Result: {self.round}, {event_name}, {timestamp-self.start_time}')
                    self.results.event_queue.put([self.round, event_name, timestamp-self.start_time]) 
                else: 
                    # we will loop back around to this future later 
                    time.sleep(0.25)
            
            if self.stop_threads is True: 
                if len(self.futures) == 0: 
                    logging.debug('all futures were accounted for; finished cleanly')
                    return 
                else: 
                    logging.debug('some futures were not able to finish: ')
                    for future,name in self.futures: 
                        logging.debug(f'(Future Name) {name} (Running) {future.running()}')
                    return 


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  functions for tracking & signaling event occurrences   #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
                       
    def countdown_timer(self, timeinterval, event): 
        print("\r")
        while timeinterval:
            mins, secs = divmod(timeinterval, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            sys.stdout.write(f"\r{timer} until {event}  ")
            time.sleep(1)
            timeinterval -= 1

    def pulse_sync_line(self, round, length): 
        # calls the function pulse_sync_line defined in the Pin class. 
        # doing it this way so from main prog, user doesn't have to worry about specifying the pin since its the same pin every time 
        # write to results 
        print("P U L S E")
        self.results.event_queue.put([round, f'pulse sync line ({length})', time.time()-self.start_time])
        self.pins['gpio_sync'].pulse_sync_line(length)
        return 'pulse', time.time(), True

    def buzz(self, buzz_type): 
        # play sound function 
        # set values for buzz length, hz, and name
        print("B U Z Z")
        if buzz_type is 'round_buzz': 
            buzz_len =   self.key_values['round_start_tone_time']
            hz =  self.key_values['round_start_tone_hz']
            name = 'round_start_tone'
            
        elif buzz_type is 'pellet_buzz': 
            buzz_len = self.key_values['pellet_tone_time']
            hz = self.key_values['pellet_tone_hz']
            name =  'pellet_tone'
            
        elif buzz_type is 'door_open_buzz': 
            buzz_len = self.key_values['door_open_tone_time']
            hz = self.key_values['door_open_tone_hz']
            name = 'door_open_tone'

        elif buzz_type is 'door_close_buzz':
            buzz_len = self.key_values['door_close_tone_time'] 
            hz = self.key_values['door_close_tone_hz']
            name = 'door_close_tone'
        
        else: 
            Exception('the specified buzz_type passed to the buzz funciton does not exist. check for spelling errors?')
            exit()
        
        # write to results 
        self.results.event_queue.put([self.round, f'{name} tone start {hz}:hz {buzz_len}:seconds', time.time() - self.start_time ])
        self.pins['speaker_tone'].buzz(buzz_len, hz) 
        self.results.event_queue.put([self.round, f'{name} tone complete {hz}:hz {buzz_len}:seconds', time.time() - self.start_time ])        
        return buzz_len, hz, name 


    def lever_event_callback(self, object, event_name, timestamp): 
        # A reference to this function is passed to monitor_lever_continuous in Lever.py. Gets called if a lever press occurs while lever.monitoring is True
        #   Arguments: (1) object is the name of the lever that was pressed 
        #              (2) event_name and timestamp contains the information we want to write to output file 
                   
        if event_name: 
            print(f'{event_name} recorded!')
            self.results.event_queue.put([self.round, event_name, timestamp-self.start_time]) # record event in event queue
        else: 
            print(f'{event_name} timed out. No press recorded for {object}.')
            # TODO/QUESTION: should i write 'no press detected' to output file? 
            # self.executor.submit(self.buzz, 'pellet_buzz')



    # # # # # # # # # # # # # # # # # # # # # # # # # #
    #               cleanup function                  #
    # # # # # # # # # # # # # # # # # # # # # # # # # #  

    def cleanup(self, finalClean = False): 
        # make sure all doors closed and no servos are running still  
        print('script cleanup!')

        self.stop_threads = True # let
        if self.executor_manager.is_alive(): # if thread is running 
            logging.debug('waiting for executor manager to finish its final loop thru the executor threads (ScriptClass.py)')
            self.executor_manager.join() # waits so last loop thru can finish 
        
        for d in self.doors: 
            self.doors[d].cleanup() # shuts doors and shuts off door servos 
        self.results.cleanup() # finishes writing stuff in event_queue to output file
        
        lever_pins = self.get_pins_of_type('lever')        
        for i in lever_pins: 
            print(f'I recorded a total of {lever_pins[i].all_lever_presses.qsize()} lever presses for {lever_pins[i].name}')
            lever_pins[i].cleanup()
        pellet_pins = self.get_pins_of_type('pellet')
        for i in pellet_pins: 
            pellet_pins[i].cleanup()
    
        if finalClean: 
            print('gpio cleanup done')
            GPIO.cleanup()
        
        return     
    

        

    
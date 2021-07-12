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


# Third Party Imports
import pandas as pd 
from concurrent.futures import ThreadPoolExecutor
import RPi.GPIO as GPIO

# Local imports 
from class_definitions.results import Results # manages output data 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.Pin import Pin # import pin class
from class_definitions.hardware_classes.pins_class.Lever import Lever # subclass to Pin
from class_definitions.hardware_classes.pins_class.Pellet import Pellet # subclass to Pin
from class_definitions.hardware_classes.Door import Door # built on top of multiple Pins

# Globals 
eventQ_lock = threading.Lock()

 
class Script(): 
    ''' 
        class Script: 
           meant for holding the information that all of the scripts have in common. 
           then, for each script, if it needs to add more it can override this parent class with a subclass 
    '''

    def __init__(self, csv_input, output_dir, key_values, pin_values=None):

        # input and output files
        self.csv_input = csv_input
        self.output_dir = output_dir
        self.results = Results(csv_input, output_dir) # Resutls Class monitors output file tasks
        
        # Setup Values of user's Input Information for running Experiment
        self.key_values = self.change_key_values(key_values, csv_input['key_val_changes'])
        
        # Setup Dictionary of Names of Pins, and create the pin as a Pin Object or Lever Object (subclass of Pin)
        self.pins = self.setup_pins_dict(pin_dict=None) # dictionary of all the individual pin objects
           
        # Group the pins up that are for controlling the doors, and pass to new Door object. 
        self.doors = self.setup_Doors() # returns dictionary for each door. 
        
        # Experiment Information 
        self.round = 0  
        self.start_time = time.time()
        
        # Thread Pool 
        self.executor = ThreadPoolExecutor(max_workers=20) 
                    
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
    
                  
    '''def setup_Food(self): # this function is only made to create a single instance of Food. Will need changing if there comes a point where more than one is needed. 
    
        food_dict = {}
        type_keywords = ['food', 'pellet']
        pins_of_food = {}
        for keyword in type_keywords:   
            pins_of_food.update(self.get_pins_of_type(keyword)) # combine dictionaries 
        
        food_dict['lever_food'] = Food(pins_of_food)
        return food_dict['lever_food'] # make instance of Food and return  '''
                    
           
    
    ''' ------------- Public Methods ------------------------'''

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
            print('\n\bye!')
            exit()
                
                    
    def countdown_timer(self, timeinterval, event): 
        print("\r")
        while timeinterval:
            mins, secs = divmod(timeinterval, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            sys.stdout.write(f"\r{timer} until {event}  ")
            time.sleep(1)
            timeinterval -= 1



    def buzz(self, buzz_type): 
        # play sound function 
        # set values for buzz length, hz, and name
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


    def pulse_sync_line(self, round, length): 
        # calls the function pulse_sync_line defined in the Pin class. 
        # doing it this way so from main prog, user doesn't have to worry about specifying the pin since its the same pin every time 
        # write to results 
        self.results.event_queue.put([round, f'pulse sync line ({length})', time.time()-self.start_time])
        self.pins['gpio_sync'].pulse_sync_line(length)
        return 

   
    def lever_event_callback(self, object, event_name, timestamp): 
        if event_name: 
            print(f'{event_name} occurred for {object}!')
            self.executor.submit(self.pulse_sync_line, self.round, length=0.25) # Pulse for Event: Lever Press 
            self.executor.submit(self.buzz, 'pellet_buzz') # play sound for lever press  
            self.results.event_queue.put([self.round, event_name, timestamp-self.start_time]) # record event in event queue
        else: 
            print(f'{event_name} timed out. No press detected for {object}.')
            # TODO/QUESTION: should i write 'no press detected' to output file? 
            self.executor.submit(self.buzz, 'pellet_buzz')

         
    def cleanup(self): 
        # make sure all doors closed and no servos are running still  
        print('script cleanup!')
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
        
        GPIO.cleanup() # cleans up all gpio pins 
       
        return     

        

    
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
from class_definitions.hardware_classes.box import Box 

# Globals 
eventQ_lock = threading.Lock()


class Script(): # each script that runs gets its own instance of Script created 
    ''' 
        class Script: 
           meant for holding the information that all of the scripts have in common. 
           then, for each script, if it needs to add more it can override this parent class with a subclass 
    '''

    def __init__(self, csv_input, output_dir, key_values):

        # input and output files
        self.box = Box() # create new box 

        
        self.csv_input = csv_input
        self.output_dir = output_dir
        self.results = Results(csv_input, output_dir, self.box.timestamp_q) # Results Class monitors output file tasks
        
        # Setup Values of user's Input Information for running Experiment
        self.key_values = self.change_key_values(key_values, csv_input['key_val_changes'])
        

        
        # Experiment Information 
        self.round = 0  
        self.start_time = time.time()
        # Update Experiemnt Information in timestamp_q
        self.box.timestamp_q.round = self.round 
        self.box.timestamp_q.round_start_time = self.start_time
        
        # Thread Pool 
        self.executor = ThreadPoolExecutor(max_workers=20) 
        self.executor_manager = threading.Thread(target=self.monitor_for_future_results, daemon=True)
        self.futures = []
        self.stop_threads = False 
#         self._setup_fulltime_threads() 

        # Event Config 
        self.onPressEvents = []
        self.noPressEvents = []
                    

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

        
    def delay(self, sec): # CHANGE: new function
        time.sleep(sec)
        return

                
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #       Functions for managing/monitoring the Thread Pool and its resulting Futures                     #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def thread_pool_submit(self, event_name, func, *args, **kwargs): 
        future = self.executor.submit(func, *args, **kwargs)   
        self.futures.append([future, event_name]) # adds to list of futures to ensure it gets written to output once it finishes 

    def monitor_for_future_results(self): 
        # separate thread 
        while True: 
            '''loop thru self.futures list(or queue?). Check if the future is done running. If it is, 
            then get its result and write them to event_queue. If it is not, then leave it be and go to the 
            next element. Repeat until the round has finished. '''
            
            for future,name in (self.futures): 
                if future.done(): # Check to see if future is done 
                    self.futures.remove([future,name]) # remove the future tuple from list of futures
                    event_name, timestamp, ifEvent = future.result() # get future's result
                    print(f'Future Result: {event_name}')
                    
                    #self.results.event_queue.put([self.round, event_name, timestamp-self.start_time]) 
                else: 
                    # we will loop back around to this future later 
                    time.sleep(0.25)

    def check_for_running_futures(self):  
        if self.stop_threads is True: 
            if len(self.futures) == 0: 
                logging.debug('all futures were accounted for; finished cleanly')
                return True 
            else: 
                logging.debug('some futures were not able to finish: ')
                for future,name in self.futures: 
                    logging.debug(f'(Future Name:){name} (Is Running:){future.running()}')
                return False 


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


    # # # # # # # # # # # # # # # # # # # # 
    #           Pin Functions             #
    # # # # # # # # # # # # # # # # # # # # 

    
    def print_pin_status(self, pins):
    
        
            

            print("\033c", end="")
            if len(pins) > 1: 
                sorted_pins = sorted(pins)
                status = []
                print('NUM PINS: ', len(pins))
                num_pins = len(pins)
                for i in range(0,num_pins-1,2):
                    print("i value: ", i)
            
                    if i+1<num_pins:
                        status += [[sorted_pins[i], GPIO.input(sorted_pins[i]),
                                    sorted_pins[i+1], GPIO.input(sorted_pins[i+1])]]
                    else:
                        status += [[sorted_pins[i], GPIO.input(sorted_pins[i].number),
                                    '', '']]
                print(tabulate(status, headers = ['pin', 'status', 'pin', 'status']))
                time.sleep(0.05)

            else: 
                data = [[pins[0], GPIO.input(pins[0])]]
                print(tabulate(data, headers=['pin', 'status']))
                time.sleep(0.05)

            try:
                while True:
                    self.print_pin_status(pins)
                    time.sleep(0.05)
            except KeyboardInterrupt:
                print('\n bye!')
                exit()


    # # # # # # # # # # # # # # # # # # # # # # # # # #
    #               cleanup function                  #
    # # # # # # # # # # # # # # # # # # # # # # # # # #  
    def new_round(self): 
        self.round += 1 
        self.box.timestamp_q.round += 1 
        self.box.timestamp_q.start_time = time.time() 

    def cleanup(self, finalClean = False): 
        # make sure all doors closed and no servos are running still  
        print('script cleanup!')

        self.stop_threads = True 
        self.check_for_running_futures() 
        '''if self.executor_manager.is_alive(): # if thread is running 
            logging.debug('waiting for executor manager to finish its final loop thru the executor threads (ScriptClass.py)')
            self.executor_manager.join() # waits so last loop thru can finish'''
         
    
    
        for object in self.box.object_list: 
            object.cleanup()


    ''' 
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
        
        return     '''
    

        

    
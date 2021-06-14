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

# Third Party Imports
import pandas as pd 
import pigpio 

# Local imports 
from class_definitions.results import Results # manages output data 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.Pin import Pin # import pin class
from class_definitions.hardware_classes.pins_class.DoorLever import Door 
from class_definitions.hardware_classes.pins_class.FoodLever import Food
# from class_definitions.hardware_classes.lever import (Door, Food) # Parent Class: Lever, Subclass: Door  


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
        self.Results = Results(csv_input, output_dir) # Resutls Class monitors output file tasks
        
        # Setup Values of user's Input Information for running Experiment
        self.key_values = self.change_key_values(key_values, csv_input['key_val_changes'])
        
        # Setup Dictionary of Names of Pins, and create Pin Classes Accordingly 
        self.pins = self.setup_pins_dict() # dictionary of all the individual pin objects
        print("ScriptClass.py pin_obj_dict test -- 'lever_door_1' is of type: ", self.pins['lever_door_1'].type)
       
        
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
        
        # create new dictionary where each element is (pin_name:Pin_class_instance)
        pin_obj_dict= {} # inialize empty dict
        
        # set the type of the pin based on the pin's name, and then create instance of Pin and append this to pin_obj_dict
        for key in pin_dict.keys(): 
            type = None # reset type to None each iteration
            # instantiate object based on type
            if 'door' in key:
                # create new Door instance and add to dictionary
                pin_obj_dict[key] = Door( key, pin_dict.get(key)) # key -> Pin pair added to dictionary
            
            elif 'food' in key: 
                pin_obj_dict[key] = Food( key, pin_dict.get(key))
            else: 
                pin_obj_dict[key] = Pin( key, pin_dict.get(key)) 
                
            '''elif 'read' in self.key:
                type = 'read'
            elif 'led' in self.key or 'dispense' in self.key :
                type = 'led '''
           
        
        print("initialized pin_obj_dict. To access a single pin object by it's name, use pin_obj_dict['name_of_pin']")
        return pin_obj_dict
    
    ''' ------------- Public Methods ------------------------'''

    def get_pins_of_type(self, type): 
        # returns pins of the specified type 
        pin_lst = []
        for p in self.pins.values(): # loop thru the pins dictionary values which contains the Pin Object
            if p.type == type: # if pin's type matches the speicified type
                pin_lst.append(p) # add to list
            else: pass # otherwise, go to next pin in the list 
        return pin_lst
                
    ''' TODO: 
    
    -threads or1 and or2, w/ target fn.override_door_1 and fn.override_door_2 
    -should be created for every Script instance, so add to __init__ 
        self.or1_tid = threading.Thread(target = fn.override_door_1, daemon=True)
        self.or2_tid = threading.Thread(target = fn.override_door_2, daemon = True)



    '''
    
    def countdown_timer(self, timeinterval, event): 
        print("\r")
        while timeinterval:
            mins, secs = divmod(timeinterval, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            sys.stdout.write(f"\r{timer} until {event}")
            time.sleep(1)
            timeinterval -= 1

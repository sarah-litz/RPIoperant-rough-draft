''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: ScriptClass.py
                    description: defines the parent class Script. This will get imported by each of the files in the run_scripts file. 
                    Allows the different scripts to define a subclass of Script, so they can inherit from this class but adjust the 
                    attributes and methods as needed. 

                    Imports all of the other components that are necessary for the running. i.e. the hardware stuff and the data analysis stuff. 
-----------------------------------------------------------------------------------------------------------------------------------'''



# TODO/QUESTION: think i need a raspberry pi at this point, so commenting these imports out
# import RPi.GPIO as GPIO
import csv
import pigpio
import GPIOEmulator as GPIO # mock raspberry pi
import json
import pandas as pd 

from class_definitions.results import Results # manages output data 

class Script(): 
    ''' 
        class Script: 
           meant for holding the information that all of the scripts have in common. 
           then, for each script, if it needs to add more it can override this parent class with a subclass 
    '''

    def __init__(self, csv_input, output_dir, key_values):

        self.csv_input = csv_input
        self.output_dir = output_dir
        self.key_values = self.change_key_values(key_values, csv_input['key_val_changes'])

        ''' INIT OUTPUT FILE ''' 
        self.Results = Results(csv_input, output_dir) # Create Results instance
        # self.output_file = self.Results.output_file # get newly generated output file from Results 
        
        # self.pi = pigpio.pi() # initalize pi 
        

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

    
    ''' ------------- Public Methods ------------------------'''


    ''' TODO: 
    
    -threads or1 and or2, w/ target fn.override_door_1 and fn.override_door_2 
    -should be created for every Script instance, so add to __init__ 
        self.or1_tid = threading.Thread(target = fn.override_door_1, daemon=True)
        self.or2_tid = threading.Thread(target = fn.override_door_2, daemon = True)



    '''
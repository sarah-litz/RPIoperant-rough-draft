''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Script.py
                    description: defines the parent class Script. This will get imported by each of the files in the run_scripts file. 
                    Allows the different scripts to define a subclass of Script, so they can inherit from this class but adjust the 
                    attributes and methods as needed. 
-----------------------------------------------------------------------------------------------------------------------------------'''


# import sys
# sys.path.append('run_scripts') # ensures that interpreter will search in this directory for modules 

# TODO/QUESTION: think i need a raspberry pi at this point, so commenting these imports out
# import RPi.GPIO as GPIO
import pigpio
import GPIOEmulator as GPIO # mock raspberry pi
import json
import pandas as pd 

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

        # instantiate corresponding output file 
        #self.output_file = self.set_output_file(self.output_file)
        # self.key_values #OrderedDict.fromkeys() # if keyVals that need tracking change, the child class will just have to override this attribute 
        # self.pi = pigpio.pi() # initalize pi 
        

    ''' ------------- Private Methods --------------------'''
    # Make changes to the key values if user added to column "key_val_changes" in csv file
    def change_key_values(self, key_values, key_val_changes): 
        if not (pd.isnull(key_val_changes)): # check if user wants to change any key values 
            key_val_changes_dict = json.loads(key_val_changes)
            for key in key_val_changes_dict: 
                if key in self.key_values: 
                    print("User requested Key Val Changes:", key_val_changes_dict)
                    key_values.update({key: key_val_changes_dict.get(key)})
                else: 
                    print(f'** you asked to change the value of "{key}" which is not listed as a value that Magazine script needs to track, so skipped this one **')
        
        return key_values

    
    ''' ------------- Public Methods ------------------------'''
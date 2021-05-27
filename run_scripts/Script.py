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

class Script(): 
    ''' 
        class Script: 
           meant for holding the information that all of the scripts have in common. 
           then, for each script, if it needs to add more it can override this parent class with a subclass 
    '''

    def __init__(self, key_value_dict):
        self.key_values = key_value_dict #OrderedDict.fromkeys() # if keyVals that need tracking change, the child class will just have to override this attribute 
        # self.pi = pigpio.pi() # initalize pi 

    def setup_pins(self): 
        pass 

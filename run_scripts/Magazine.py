
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Magazine.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# Third party imports 
from collections import OrderedDict

# Local imports 
from class_definitions.ScriptClass import Script # import Script # import the parent class 


# class Magazine(Script):  

#    def __init__(self, csv_input, output_dir): # if no key_val_changes passed in then it defaults to None 
               
#        ''' init defautly key values  '''
#        self.key_values = get_key_values()
        
#        super().__init__(csv_input, output_dir, self.key_values) # initialize attributes of parent class (defined in Script.py)

#        ''' INIT OUTPUT FILE ''' 
        # self.Results = Results(csv_input, output_dir) # Create Results instance
        # self.output_file = self.Results.output_file # get newly generated output file from Results 


''' ~ ~ ~ functions for getting default values! ~ ~ ~  
        Defined Here: values for pins, key values '''
        
def get_pin_values(): 
    ''' PIN VALUES DEFINED HERE: if left empty, then default values (from operant_cage_settings_defaults) are used. '''
    pins = {}
    return pins 

def get_key_values(): 
    # not defined inside of Magazine class for more accessibility when testing individual scripts 
    ''' DEFAUTL KEY VALUES DEFINED HERE '''
    return OrderedDict([('num_rounds', 15), ('round_time',90), 
                                        ('timeII',2), ('timeIV',2), 
                                        ('pellet_tone_time',1), ('pellet_tone_hz',2500), 
                                        ('door_close_tone_hz',7000), ('door_open_tone_time',1), ('door_open_tone_hz',10000),
                                        ('round_start_tone_time',1), ('round_start_tone_hz',5000)
                                    ]) 




def run_script(csv_input, output_dir):  # csv_input is the row that corresponds with the current script getting run 
 
    
    Magazine = Script(csv_input, output_dir, get_key_values()) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 

    # setup pins 
    # setup experiment
    # def round_buzz, pellet_buzz, door_open_buzz, door_close_buzz
    # start monitor workers 
    # reset the chamber 
    # start timing 
    # pulse synch line 
    
    
    print(f"setup finished, starting experiment with these key values: \n {Magazine.key_values}: \n")
    for count in range(0, int(Magazine.key_values['num_rounds'])): 

        print("round #",count+1)

    return True 
    



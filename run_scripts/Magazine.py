
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Magazine.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''

from collections import OrderedDict
from run_scripts.Script import Script # import the parent class 
import json



class Magazine:  

    def __init__(self, key_val_changes=None): # if no key_val_changes passed in then it defaults to None 
        
        self.Script = Script() # every script class gets an instance of Script class which contains the functions that apply to all the scripts  

        ''' define default key values here: '''
        self.key_values = OrderedDict([('num_rounds', 15), ('round_time',90), 
                                        ('timeII',2), ('timeIV',2), 
                                        ('pellet_tone_time',1), ('pellet_tone_hz',2500), 
                                        ('door_close_tone_hz',7000), ('door_open_tone_time',1), ('door_open_tone_hz',10000),
                                        ('round_start_tone_time',1), ('round_start_tone_hz',5000)
                                    ]) # initalize key value dictionary with default values 


        ''' make changes to the key values if user specified that in the csv file '''
        if (key_val_changes != None): # check if user wants to change any key values 
            # adjust the key_values dictionary to change the default values to the desired changed values 
            key_val_changes_dict = json.loads(key_val_changes)
            for key in key_val_changes_dict: 
                if key in self.key_values: 
                    print("User requested Key Val Changes:", key_val_changes_dict)
                    self.key_values.update({key: key_val_changes_dict.get(key)})
                else: 
                    print(f'** you asked to change the value of "{key}" which is not listed as a value that Magazine script needs to track, so skipped this one **')

        
        
def start(csv_input):  # csv_input is the row that corresponds with the current script getting run 

    current_script = Magazine(csv_input['key_val_changes']) # initalizes instance of MagazineScript with the user defined values for the script 

    print("setup finished, starting experiment now...\n")
    for count in range(0, int(current_script.key_values['num_rounds'])): 

        print("round #",count+1)

    return True 
    




''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Magazine.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''

from collections import OrderedDict
from run_scripts.ScriptClass import Script # import the parent class 
from run_scripts.ResultsClass import Results # manages output data 


class Magazine(Script):  

    def __init__(self, csv_input, output_dir): # if no key_val_changes passed in then it defaults to None 
        
       
        ''' INIT DEFAULT KEY VALUES '''
        ''' define default key values here: '''
        self.key_values = OrderedDict([('num_rounds', 15), ('round_time',90), 
                                        ('timeII',2), ('timeIV',2), 
                                        ('pellet_tone_time',1), ('pellet_tone_hz',2500), 
                                        ('door_close_tone_hz',7000), ('door_open_tone_time',1), ('door_open_tone_hz',10000),
                                        ('round_start_tone_time',1), ('round_start_tone_hz',5000)
                                    ]) 
        
        super().__init__(csv_input, output_dir, self.key_values) # initialize attributes of parent class (defined in Script.py)


        ''' INIT OUTPUT FILE ''' 
        self.Results = Results(csv_input, output_dir) # Create Results instance
        self.output_file = self.Results.output_file # get newly generated output file from Results 



def start(csv_input, outputdir):  # csv_input is the row that corresponds with the current script getting run 

    current_script = Magazine(csv_input, outputdir) # initalizes instance of MagazineScript with the user defined values for the script 

    print(f"setup finished, starting experiment with these key values: \n {current_script.key_values}: \n")
    for count in range(0, int(current_script.key_values['num_rounds'])): 

        print("round #",count+1)

    return True 
    



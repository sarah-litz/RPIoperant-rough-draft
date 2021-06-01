
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Results.py
                    description: 
                    
                    instantiated in
-----------------------------------------------------------------------------------------------------------------------------------'''

import datetime
import os
import csv
from pathlib import Path

class Results(): 
    

    def __init__(self, csv_input, output_dir): # pass in info from input csv file, and the (optional) directory for where user wants output file to go
        
        ''' requires that an output file will get found or created when a new Results instance is made'''
        self.output_file = self.generate_output_file(csv_input, output_dir)


    ''' --------- Private Methods ----------- '''    
    def generate_output_file(self, csv_input, output_dir): # called at instance declaration only (called from w/in class, no need to call from different module)
            
        # autogenerate output file name 
        date = datetime.datetime.now()
        fdate = '%s_%s_%s__%s_%s_'%(date.month, date.day, date.year, date.hour, date.minute)

        user = csv_input['user']
        script_name = csv_input['script']
        vole = csv_input['vole']
        fname = fdate+f'_{script_name}_vole_{vole}.csv'

        ''' set filepath '''
        if output_dir != None: # check if user specified the directory 
            fp = os.path.join(output_dir, fname)  
        else: 
            # DEFAULT DIRECTORY 
            defaultfp = Path('/home/pi/test_outputs/') 

            # if it does not exist, then create it
            defaultfp.mkdir(parents=True, exist_ok=True) # makes directory if it does not exist 
            fp = os.path.join(defaultfp, fname)
        
        ''' open file and write header with general experiment information '''
        with open(fp, 'w') as output_file: # output_file is the new file object 
            writer = csv.writer(output_file, delimiter = ',')
        
            writer.writerow(['user: %s'%user, 'vole: %s'%vole, 'date: %s'%date,
            'experiment: %s'%script_name, 'Day: %i'%date.day, ''''Pi: %s'%socket.gethostname()'''])

        with open(fp, 'r') as output_file: 
            print("\noutput filepath:", output_file)
            for line in output_file: 
                print(line)

        return output_file # sets self.output_file to this value 
    
    '''--------------------------------------------------'''
    '''    ------------ Public Methods -------------     '''
       
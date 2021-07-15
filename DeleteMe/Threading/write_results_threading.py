


# local imports  
from class_definitions.hardware_classes.pins_class.Lever import Lever # import pin class
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.Results import Results # manages output data 


#!/usr/bin/python3
import argparse
from types import TracebackType 
import pandas as pd
import importlib
import sys, traceback, time, os  
import threading 



def set_output_dir(output_loc):
    if output_loc:
        if not os.path.isdir(output_loc):
            selection  = input(f'\n\nhmmm, output location {output_loc} doesnt exist. make it? \ne (exit) \ny (make new directory) \nn (use default output location /home/pi/test_outputs/)\n\n')
            selection = selection.lower()
            if not selection in ['y', 'n','e']:
                print('invalid choice. see ya!')
                exit()
            elif selection == 'y':
                os.mkdir(output_loc)
                outputdir = output_loc 
            elif selection == 'n':
                print('ok, saving to default loc.')
                outputdir = None
                # time.sleep(2) # TODO/QUESTION: this line was in inital code. Why do we need this? 
            else:
                exit()
        else:
            outputdir = output_loc
    else:
        outputdir = None

    return outputdir



def startup(): 
    
    # prompt user for experiment input 
    print('welcome\n')

    inputfp = 'default.csv'
    outputdir = set_output_dir('defaultfp')
    
    print("input filepath:", inputfp)
    print("output directory:", outputdir)
    
    inputdf = pd.read_csv(inputfp) 
    csv_row = inputdf.loc[1] # get 1st row 
    Results(csv_row, outputdir)


def main(): 

    results = startup()
    writer_thread = threading.Thread(target=results.write_results, args=(), daemon=True).start()


try: main() 
except KeyboardInterrupt: print('interrupt, shutting down')
except Exception: 
        traceback.print_exc(file=sys.stdout)
sys.exit(0)
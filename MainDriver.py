''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: MainDriver.py
                                                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3
import argparse
import ScriptDriver 
import pandas as pd
import os 
import time 


def set_input_fp(csv_in): 
    if csv_in: inputfp = csv_in # if user entered arg for csv_in, set inputfp to arg 
    else: inputfp = 'default.csv' # if no arg entered, then set input file to default 
    
    if not os.path.isfile(inputfp):
        print('not a valid csvfile. double check that filepath! see ya.')
        exit()
    else: return inputfp


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

    ''' TODO: if we want to go up a directory to store the output file, could potentially use these commands.
    os.chdir("..")
    print(os.path.abspath(os.curdir)) '''


def main(): 
    
    # prompt user for experiment input 
    print('welcome\n')

    # TODO: args parse thing 
    # check if user entered in command line arguments. If entered, then check validity of the arguments. 
        # argument #1 must be name of an input file 
        # argument #2 must be name of a directory where output files will be placed 
    
    parser = argparse.ArgumentParser(description='input io info')
    parser.add_argument('--csv_in', '-i',type = str, 
                    help = 'where is the csv experiments file?', # if user enters -h (for help), displays this string 
                    action = 'store')
    parser.add_argument('--output_loc','-o', type = str, 
                    help = 'where to save output files',
                    action = 'store')
    args = parser.parse_args()

    print("args:" , args)

    inputfp = set_input_fp(args.csv_in)
    outputdir = set_output_dir(args.output_loc)
    
    print("input filepath:", inputfp)
    print("output directory:", outputdir)
    

    inputdf = pd.read_csv(inputfp) 
    print(inputdf)

    ''' transfer control to ScriptDriver.py '''
    ScriptDriver.startExperiment(inputdf, outputdir)

    # inputdf = InputFile.getInputFile()
    # if inputdf.empty: print('data frame is empty'); exit() # nothing in file - alerts user and exits  

    # prompt user for experiment output file 
    # outputfp = OutputFile.getOutputFile()
    
    # ScriptDriver.startExperiment(inputdf, outputfp)
    # transfer control to module in charge of the different scripts. Pass the inputdf and the outputFile to this module. 
        # loop through all the scripts that the user wants to have run
        # then we will transfer control to module of specified script 
        # will potentially need to pass the current row of the dataframe if we need that info to run the script 


        


main() #TODO: get rid of main() when done. Just makes it easier for me to see where my main function is as im working so leaving it for now. 
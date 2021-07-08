''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: MainDriver.py
                                                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3
import argparse
from types import TracebackType 
import pandas as pd
import importlib
import sys, traceback, time, os  



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
                print('ok, saving to default loc.') # default location is set by results.py
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


def run_next_check(module): 
    checkIn = False 
    while True: 
        userIn = input(f'would you like to run {module}? (y/n)') 
        if (userIn == 'y' or userIn == 'yes'): 
            return True 
        if (userIn == 'n' or userIn == 'no'): 
            return False 
        else: 
            print('sorry, I dont recognzie that input. please only enter a y or an n')



def startup(): 
    
    # prompt user for experiment input 
    print('welcome\n')

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


    ''' -------- LOAD IN MODULE OF NXT SCRIPT TO RUN ----------- ''' 
    # looping through all the scripts that the user wants to have run
    # for each script, transfers control to module of specified script 
    scriptList = inputdf['script'].copy().tolist() 
    print(scriptList)
    count = 0 # counter to loop thru script list 
    
    # while(len(scriptList) > 0): # need to comment this out for testing so doesn't end up in a endless loop. But will use this while loop instead of the foor loop later on. 
    for x in scriptList:
         
        # make sure that 'script' is a valid module in run_scripts ( use the importlib.util.find_spec() or actually might be spec_from_file_location() )
        print('-------------------')
        exists = os.path.exists(f'run_scripts/{scriptList[count]}.py')
        if exists: 
            # check if user wants to run next script  
            if (run_next_check(scriptList[count]) == False ): 
                print(f'see you l8er')
                exit()
            else: 
            # load in new script 
                print(f'loading in new script: {scriptList[count]}')
                spec = importlib.util.spec_from_file_location(scriptList[count], 'run_scripts/' + f'{scriptList[count]}.py') # get new module's file specs 
                module = importlib.util.module_from_spec(spec) 
                spec.loader.exec_module(module)
    
                # get current row of dataframe 
                csv_row = inputdf.loc[count]
                module.run(csv_row, outputdir)

        else: 
            print(f'could not locate the following module in the run_scripts folder: {scriptList[count]}' )

        count+=1 # increment counter so we can get the next script from scriptList
        nxt = run_next_check(scriptList[count]) # checks if user wants to run next script 
        if not nxt: 
            print('exiting now')
            return 

        # run next thing in scriptLst 
            # TODO: check that script is done 
            # if done, then remove from scriptList
            # else, ??? 
            # when script is finished running, make sure that it gets removed from this list! 


def main():  # TODO: get rid of main() function at somepoint, probably
    
    try: 
        startup() 
    except KeyboardInterrupt: 
        print("keyboard interrupt detected, shutting down.")
    except Exception: 
        traceback.print_exc(file=sys.stdout)
    
    # TODO: add clean up function call here!! Ensures that operant box doesn't get stuck running. (i.e. prevent a servo from endlessly spinning)
    sys.exit(0)


if __name__ == "__main__": # must be running MainDriver directly
    main()


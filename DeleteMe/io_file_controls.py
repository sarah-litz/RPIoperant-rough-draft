''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: io_file_controls.py
                                                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3
import os
import pandas as pd

class InputFile: 

    def __init__(self, inputfp):
        self.dataframe = pd.read_csv(inputfp) 

        # for each line of the dataframe, in
            

    def getInputFile():
        ''' ------- getInputFile description: 
        getInputFile retrieves the user entered data on the series of scripts that the user would like to run. If it successfully finds the input file (or gets it from command line), 
        it will return the desired dataframe to the main function.
        --------'''

        userin = input(f"Would you like to run the experiment with the default values specified in InputDataFiles/default.csv? (y/n)\n")
        if userin=='y': 
            # open default file (if the default filename is ever changed, must be updated here as well)
            if (os.path.exists('InputDataFiles/default.csv')): # check that the default file exists 
                print('Default file found! Here are the first couple lines of the file: \n')
                filepath = 'InputDataFiles/default.csv'
                df = pd.read_csv(filepath)
                print(df.head())
                return df 
            else: 
                print('Sorry, seems like there was a problem finding the default file. Check that it is in the following folder: InputDataFiles\n')
                exit()

        if userin=='n': 

            # TODO: change user input to argparse ( specifically for the input and output file locations )
            userin2 = input('Please enter a 1 or a 2 for how you would like to enter your input data: \n (1) enter new csv file name (must exist in the InputDataFiles folder) \n (2) manually enter in data from the command line (not yet implemented) \n')
            if ( userin2 == '1'): 
                filepath = 'InputDataFiles/' + input('Enter in the file name in the following format: customFileName.csv \n') # concatenate strings to form the file path (we are assuming that file is in the folder InputDataFiles)
                if (os.path.exists(filepath)): # check that the specified file exists 
                    print(f'{filepath} found! Here are the first couple of lines of the file: \n')
                    df = pd.read_csv(filepath)
                    print(df.head())
                    return df 
                else: 
                    print(f'{filepath} does not exist in the InputDataFiles folder! Please create the file and then run the program again.')
                    exit()
            if ( userin2 == '2' ): 
                # column names from csv file: date,run_time,vole,script,user,rounds,rounds_completed,var_changes,done,experiment_status,day
                # TODO/QUESTION: not positive on what data to prompt user for here?? may need to add more. 
                    # TODO: how do we allow user to change key values here? 

                date = []; runtime = []; vole = []; script = []; user = []; rounds = []; rounds_completed = []; var_changes = []; done = []; experiment_status = []; day = []; 

                while True: # loops through each of the attributes we want in the dataframe 
                    vole.append(input("Enter vole number: "))
                    script.append(input("Enter name of script to run: "))
                    user.append(input("Enter your name: "))
                    rounds.append(input("Enter number of rounds to run experiment: "))
                    
                    # check to see if user is finished adding data 
                    if ( input(" Would you like to add another? (y/n) ") == 'y' ): continue
                    else: break # TODO: invalid entry (user does not put y or n)
                
                # create dataframe from lists 
                voleSeries = pd.Series(vole); scriptSeries = pd.Series(script); userSeries = pd.Series(user); roundsSeries = pd.Series(rounds) # convert lists to series 
                frame = { 'vole': voleSeries, 'script': scriptSeries, 'user': userSeries, 'rounds': roundsSeries} 
                df = pd.DataFrame(frame) # make dataframe out of series 
                print(df.head()) 
                return df
                    
            else: exit()

        else: 
            print('invalid input, please put just the letter y or n. exiting for now (might add feature where this does not exit later) \n')
            exit()



class OutputFile: 
    
    def getOutputFile(): 
        '''------------ getOutputFile description: 
        Prompts user for where they would like output to go (must be in the OutputDataFiles folder). If file already exists, returns the filepath, else will create a new file and return filepath. 
        the filepath will be passed to the scripts, and the scripts will be directed to write their output to this file. 
        ---------------'''
        # TODO: autogenerated file names (reference existing code) <date><time><exprmnt><voleNumber>
            # don't need an option for users to input a filename here 
        # one output file per Script run 
        print('\n\n What is the name of the file you would like the results to be written to (file must be in the folder OutputDataFiles)? If the file does not exist, then one will automatically be created.')
        filepath = 'OutputDataFiles/' + input('Enter in the file name in the following format: customFileName.csv \n') # concatenate strings to form the file path (we are assuming that file is in the folder OutputDataFiles)
        if (os.path.exists(filepath)): # check that the specified file exists 
            print(f'{filepath} found! Experiment is good2go. \n')
            return filepath
        else: 
            with open(filepath, 'w') as fp:  # file did not exist so it automatically creates it 
                pass #TODO: write header to output file 
            print(f'{filepath} did not exist in OutputDataFiles, so I went ahead and created it for you! Experiment is good2go.')
            return fp

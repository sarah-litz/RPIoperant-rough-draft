''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: ScriptDriver.py
                                                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
import importlib
import os
from collections import OrderedDict



class Script(): 
    ''' 
        class Script: 
           meant for holding the information that all of the scripts have in common. 
           then, for each script, if it needs to add more it can override this parent class to change keyVals 
    '''
    def __init__(self, scriptName):
        self.key_values = OrderedDict.fromkeys(["num_rounds","repititions", "sets", "round_time"]) # if keyVals that need tracking change, the child class will just have to override this attribute 
                        # TODO: lookup documentation for python class definitions 
    #def get_key_values(self): 
    #    return self.key_values
    def get_key_value(self, key): 
        # returns the value that is associated with 'key'
        return self.key_values[key]
    def set_key_values(self): # change the key values from their default ones 
        # !! Reference: 
        #   def user_modify_module_key_values(self) in CSV_file_functions.py 
        pass 
        # call to change keyVals (do i need fnctn for this? or should i just do this inline idk)
    

        
        

def startExperiment(inputdf, outputfp): # (input dataframe, output filepath)

    print("input dataframe head: ", inputdf.head())
    print(outputfp)

    # module in charge of the different scripts. Pass the inputdf and the outputFile to this module. 
        # loop through all the scripts that the user wants to have run
        # then we will transfer control to module of specified script 
        # will potentially need to pass the current row of the dataframe if we need that info to run the script 

    scriptList = inputdf['script'].copy().tolist() # need to make copy() to manipulate 
    print(scriptList)
    count = 0 # counter to loop thru script list 
    
    # while(len(scriptList) > 0): # need to comment this out for testing so doesn't end up in a endless loop. But will use this while loop instead of the foor loop later on. 
    for x in scriptList:
         
        # make sure that 'script' is a valid module in run_scripts ( use the importlib.util.find_spec() or actually might be spec_from_file_location() )
        print('-------------------')
        exists = os.path.exists(f'run_scripts/{scriptList[count]}.py')
        if exists: 
            
            # instantiate new object of class Script. This will get passed to module 
            newScript = Script('{scriptList[count]}')
            print(newScript)
            # print("Key Values:", newScript.get_key_values())

            print(f'loading in new script: {scriptList[count]}')
            spec = importlib.util.spec_from_file_location(scriptList[count], 'run_scripts/' + f'{scriptList[count]}.py') # get new module's file specs 
            module = importlib.util.module_from_spec(spec) 
            spec.loader.exec_module(module)
            module.start(newScript)
        else: 
            print(f'could not locate the following module in the run_scripts folder: {scriptList[count]}' )

        count+=1 # increment counter so we can get the next script from scriptList
        
        # run next thing in scriptLst 
        # when script is finished running, make sure that it gets removed from this list! 




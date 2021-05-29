''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: ScriptDriver.py
                description: this file is imported by MainDriver.py. The startexperiment function is called by MainDriver. 
                Purpose of this file is to perform the inline import of a file based on what the user specified in <inputdf> in the run_scripts folder.
                If the user entered in a list of scripts to run, that list will be looped thru and executed in that order. 
-----------------------------------------------------------------------------------------------------------------------------------'''
import importlib
import os



def startExperiment(inputdf, outputfp): # (input dataframe, output filepath)

    print("input dataframe head: ", inputdf.head())
    print(outputfp)

    # module in charge of the different scripts. Pass the inputdf and the outputFile to this module. 
        # loop through all the scripts that the user wants to have run
        # then we will transfer control to module of specified script 
        # will potentially need to pass the current row of the dataframe if we need that info to run the script 

        # TODO: before going to the next inputdf['script'], check with the user that they want to run the next script. 

    scriptList = inputdf['script'].copy().tolist() # need to make copy() to manipulate 
    print(scriptList)
    count = 0 # counter to loop thru script list 
    
    # while(len(scriptList) > 0): # need to comment this out for testing so doesn't end up in a endless loop. But will use this while loop instead of the foor loop later on. 
    for x in scriptList:
         
        # make sure that 'script' is a valid module in run_scripts ( use the importlib.util.find_spec() or actually might be spec_from_file_location() )
        print('-------------------')
        exists = os.path.exists(f'run_scripts/{scriptList[count]}.py')
        if exists: 
            # load in new script 
            print(f'loading in new script: {scriptList[count]}')
            spec = importlib.util.spec_from_file_location(scriptList[count], 'run_scripts/' + f'{scriptList[count]}.py') # get new module's file specs 
            module = importlib.util.module_from_spec(spec) 
            spec.loader.exec_module(module)

            # get current row of dataframe 
            csv_row = inputdf.loc[count]
            module.start(csv_row)

        else: 
            print(f'could not locate the following module in the run_scripts folder: {scriptList[count]}' )

        count+=1 # increment counter so we can get the next script from scriptList
        
        # run next thing in scriptLst 
        # TODO: check that script is done 
        # if done, then remove from scriptList
        # else, ??? 
        # when script is finished running, make sure that it gets removed from this list! 




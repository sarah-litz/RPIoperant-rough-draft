#!/usr/bin/python3
import os
import pandas as pd
import ScriptDriver 



def testScriptDriver(): 

    # get input file 
    if (os.path.exists('InputDataFiles/default.csv')): # testing with default file  
        filepath = 'InputDataFiles/default.csv'
        inputdf = pd.read_csv(filepath)

    else: 
        raise Exception(' testScriptDriver() error: could not find the default input file')


    # get output file 
    if (os.path.exists('OutputDataFiles/default.csv')): # testing with default file 
        
        filepath = 'OutputDataFiles/default.csv'
        outputfp = open(filepath, 'w')
    
    else: 
        raise Exception(' testScriptDriver() error: could not find the default output file')
    

    # call ScriptDriver
    ScriptDriver.startExperiment(inputdf, outputfp)


def main():
    testScriptDriver()


main()

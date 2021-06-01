#!/usr/bin/python3
import csv
import os
import pandas as pd
from pathlib import Path
import json
import ScriptDriver
import sys
import run_scripts.Magazine as Magazine

SCRIPTLIST = ["Magazine", "magazine", "Door_test"]


def setup_vals(): 
    csv_input = 'default.csv'
    outputdir =  Path('/home/pi/test_outputs/') 
    print("path to csv file:", csv_input)
    print("output to:", outputdir)
    return csv_input, outputdir


def default_csv_vals(script): 
    csv_input = {'vole':'000','day':1, 'script':script,
                    'user':'Test User'}
    return csv_input


def get_Vole_and_User(): 
    no_user = True
    while no_user:
        user = input('who is doing this experiment? \n')
        check = input('so send the data to %s ? (y/n) \n'%user)
        if check.lower() in ['y', 'yes']:
            no_user = False
    no_vole = True
    while no_vole:
        vole = input('Vole number? \n')
        check = input('vole# is %s ? (y/n) \n'%vole)
        if check.lower() in ['y', 'yes']:
            no_vole = False
    return user,vole


def isTestRun(): 
    test_run = input('is this just a quick test run? if so, we will just do 1 round. (y/n)\n')
    if test_run.lower() in ['y', 'yes']:
        print('ok, test it is!')
        return True
    else: 
        return False 


def testMagazine(csv_input=None, outputdir = '/home/pi/test_outputs/'): 
    if ( csv_input == None ): 
        csv_input = default_csv_vals('Magazine')
    key_values = (Magazine.get_key_values()) # get default key values
    if isTestRun(): 

        key_values['num_rounds'] = 5
        key_values['round_time'] = 20


    else: 

        user,vole = get_Vole_and_User()        

        day = input('Which magazine training day is this? (starts at day 1)\n')
        day = int(day)
        
        csv_input['script'] = 'Magazine'
        csv_input['vole'] = vole
        csv_input['user'] = user
        
        # outputdir = '/home/pi/Operant_Output/script_runs/' # TODO/QUESTION: I was finding two different paths as potential default filepaths?? which one should i use


    csv_input['key_val_changes'] = json.dumps(key_values) # convert dict to string 
    Magazine.start(csv_input, outputdir) 


def main():
    if __name__ == "__main__":
        print(f"Arguments count: {len(sys.argv)}")
        for i, arg in enumerate(sys.argv):
            
            print(f"Argument {i:>6}: {arg}")

            if arg in SCRIPTLIST: 
                print(f'\nRunning {arg} directly, please enter relevant info.')
                
                if ( arg == "magazine" or arg == "Magazine"): 
                    testMagazine()

                else: 
                    print(f' OOPS there is nothing calling a test function for {arg} in the main function ')
                    if (input('would you like to exit? (y/n) ') == 'y'): 
                        exit() 

            else: 
                print(f'the script {arg} does not exist. Did you forget to add it to SCRIPTLIST in TestDriver.py?')


main()

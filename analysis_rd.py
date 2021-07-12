
''' --------------------------------------------------------------------------------------------------------------------------------                    
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3


import pandas as pd 
import csv
import sys
from pathlib import Path


''' Data Analysis Functions ''' 
        # TODO/LEAVING OFF HERE!! 
        # probably first want to better format how I am writing to the output files cause looks not gr8 rn. 
def analysis(): 
    
    print("something will happen here to analyze the data but idg what that is yet. (from resutls.py)")
    # Read In Data 
    '''with open('defaultfp/7_1_2021__18_59__Magazine_vole_1.0.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader: 
            print(row) 
            print(row[0])
            # print(csv_reader[1])'''
    df = pd.read_csv('defaultfp/7_7_2021__12_47__Magazine_vole_1.0.csv', skiprows=1) # does not read the header into the dataframe 
    print(df)
    print("\n")
    pellet_latency(df)
    by_round(df)
    
    
def pellet_latency(df): 

    pellet_events = df.loc[df['Event'].str.contains("lever press")]
    print(pellet_events)

def by_round(df): 

    num_rounds = df['Round'].nunique()
    for i in range(1, num_rounds): # skips round 0 
        leverdf = df.loc[df['Event'].str.contains("lever")]
        # take difference between lever press and lever out time 
        lever_out = leverdf.loc[leverdf['Event'].str.contains("out")]
        print("lever out: ", lever_out['Time'])
        
        lever_press = leverdf.loc[leverdf['Event'].str.contains("press")]
        print('lever press: ', lever_press['Time'])
        
        timediff = float(lever_press['Time']) - float(lever_out['Time'])
        print("time difference: ", timediff)
        print("formatted time difference:", "{:.2f}".format(timediff))
        # record the time difference for each round 
        
        # print(leverdf['Time'])
        
    

analysis()
        











'''from class_definitions.results import Results # manages output data 


def setup_results(): 
    # prompt user for experiment input 
    print('welcome\n')
    inputfp = 'default.csv'
    outputdir = ('defaultfp')
    print("input filepath:", inputfp)
    print("output directory:", outputdir)
    inputdf = pd.read_csv(inputfp) 
    csv_row = inputdf.loc[1] # get 1st row 
    return Results(csv_row, outputdir)


def analysis(): 
    results = setup_results() 
    with open(results.filepath) as f: 
        reader = csv.reader(f)
        header_row = next(reader)
        print(header_row)

analysis()'''


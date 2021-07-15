
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
    
    # Read In Data 
    '''with open('defaultfp/7_1_2021__18_59__Magazine_vole_1.0.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader: 
            print(row) 
            print(row[0])
            # print(csv_reader[1])'''
    df = pd.read_csv('defaultfp/7_12_2021__13_19__Magazine_vole_1.0.csv', skiprows=1) # does not read the header into the dataframe 
    # print(df)
    print("\n")
    # pellet_latency(df)
    # by_round(df)
    summary(df)
    
    
def pellet_latency(df): 

    pellet_events = df.loc[df['Event'].str.contains("lever press")]
    print(pellet_events, '\n')


def summary(df): 
    
    summary_dict = {}
    
    num_rounds = df['Round'].nunique() # number of rounds 
    summary_dict["number of rounds"] = [num_rounds]
    
    lever_presses = df.loc[df['Event'].str.contains("press")]
    total_lever_presses = len(lever_presses) # total number of lever presses detected
    summary_dict["Total Number of Lever Presses"] = [total_lever_presses]
    
    no_press_rounds = num_rounds - total_lever_presses
    summary_dict["Number of Rounds without a Press"] = [no_press_rounds]
    
    proportion_nopress_rounds = no_press_rounds / num_rounds
    summary_dict["Proportion of Rounds with NO Lever Press"] = [proportion_nopress_rounds]
    
    percent_press_rounds = total_lever_presses / num_rounds
    summary_dict["Percent of Rounds with a Lever Press"] = [percent_press_rounds]
    
    
    # print("Summary Dictionary: ", summary_dict)
    summary_df = pd.DataFrame(data = summary_dict)
    print(summary_df)

    
def by_round(df): 

    num_rounds = df['Round'].nunique()
    for i in range(1, num_rounds): # skips round 0 
        round_df = df.loc[df['Round']==(i)] 
        print(f'~ ~ ~ Round #{i} ~ ~ ~')
        leverdf = round_df.loc[round_df['Event'].str.contains("lever")]
        # take difference between lever press and lever out time 
        lever_out = leverdf.loc[leverdf['Event'].str.contains("out")]
        timeI = float(lever_out['Time'])
        print("lever out: ", timeI)
        
        if leverdf['Event'].str.contains("press").any(): 
            lever_press = leverdf.loc[leverdf['Event'].str.contains("press")]
            timeII = float(lever_press['Time'])
            print('lever press: ', timeII)
        
        else: 
            # there was no lever press in this round 
            lever_in = leverdf.loc[leverdf['Event'].str.contains("retracted")]
            timeII = float(lever_in['Time'])
            print("No Lever Press. Lever Retracted: ",timeII)
        
        
        timediff = timeII - timeI
        print("time difference: ", timediff)
        timediff_formatted = "{:.2f}".format(timediff)
        print("formatted time difference:", timediff_formatted)
        print("\n")
        
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


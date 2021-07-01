
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Results.py
                    description: 
                    
                    instantiated in
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3


import pandas as pd 
import csv
from pathlib import Path

from class_definitions.results import Results # manages output data 


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

analysis()


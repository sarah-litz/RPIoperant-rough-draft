
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: AnalyzeResults.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# Third Party Imports 
import pandas as pd 


class Analysis(): 
    
    def __init__(self, header, filepath): 
        self.header_df = pd.read_csv(filepath, delimiter=',', nrows=1) # reads only the first row
        self.df = pd.read_csv(filepath, skiprows=1) # reads everything but the first row 
        
        self.user = header[0]
        self.script_name = header[1]
        self.vole = header[2]
        
        print(self.user, self.script_name, self.vole)
        print(self.df)
        
    
    def summary(self):

        summary_dict = {}
        
        num_rounds = self.df['Round'].nunique() # number of rounds 
        summary_dict["number of rounds"] = [num_rounds]
        
        lever_presses = self.df.loc[self.df['Event'].str.contains("press")]
        total_lever_presses = len(lever_presses) # total number of lever presses detected
        summary_dict["Total Number of Lever Presses"] = [total_lever_presses]
        
        no_press_rounds = num_rounds - total_lever_presses
        summary_dict["Number of Rounds without a Press"] = [no_press_rounds]
        
        proportion_nopress_rounds = no_press_rounds / num_rounds
        summary_dict["Proportion of Rounds with NO Lever Press"] = [proportion_nopress_rounds]
        
        percent_press_rounds = total_lever_presses / num_rounds
        summary_dict["Percent of Rounds with a Lever Press"] = [percent_press_rounds]
        
        summary_df = pd.DataFrame(data = summary_dict)
        print(summary_df)
        return summary_df
     
    
     
    def by_round(self): 
        num_rounds = self.df['Round'].nunique()
        for i in range(1, num_rounds): # skips round 0 
            round_df = self.df.loc[self.df['Round']==(i)] 
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
    
    
    def pellet_latency(self, df): 
        pellet_df = df.loc[:, 'Event']
        # print(pellet_df.loc['pellet dispensed', 'pellet retrieved'])
        # print(pellet_df.head())
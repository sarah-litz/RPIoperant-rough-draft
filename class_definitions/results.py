
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Results.py
                    description: 
                    
                    instantiated in
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

import datetime
import os
import csv
from pathlib import Path
from queue import Queue, Empty
import threading
import pandas as pd
import socket




class Results(): 
    
    def __init__(self, csv_input, output_dir): # pass in info from input csv file, and the (optional) directory for where user wants output file to go
        
        ''' requires that an output file will get found or created when a new Results instance is made'''
        self.filepath = self.generate_output_file(csv_input, output_dir)
        self.event_queue = Queue()
        self.event_lock = threading.Lock()
        self.writer_thread =  threading.Thread(target=self.monitor_for_event, args=(), daemon=True)
        self.stop_threads = False 

    ''' --------- Private Methods ----------- '''    
    def generate_output_file(self, csv_input, output_dir): # called at instance declaration only (called from w/in class, no need to call from different module)
            
        # autogenerate output file name 
        date = datetime.datetime.now()
        fdate = '%s_%s_%s__%s_%s_'%(date.month, date.day, date.year, date.hour, date.minute)

        user = csv_input['user']
        script_name = csv_input['script']
        vole = csv_input['vole']
        fname = fdate+f'_{script_name}_vole_{vole}.csv'

        ''' set filepath '''
        if output_dir != None: # check if user specified the directory 
            fp = os.path.join(output_dir, fname)  
        else: 
            # DEFAULT DIRECTORY 
            defaultfp = Path('defaultfp') 

            # if it does not exist, then create it
            defaultfp.mkdir(parents=True, exist_ok=True) # makes directory if it does not exist 
            fp = os.path.join(defaultfp, fname)
        
        ''' open file and write header with general experiment information '''
        with open(fp, 'a') as output_file: # output_file is the new file object 
            writer = csv.writer(output_file, delimiter = ',')
        
            writer.writerow([f'(EXPERIMENT INFO) user: {user}, vole: {vole}, date: {date}, experiment: {script_name}, Day: {date.day}, Pi: {socket.gethostname()},'])
            writer.writerow(['Round', 'Event', 'Time'])
            
            
        with open(fp, 'r') as output_file: 
            print("\noutput filepath:", output_file)
            for line in output_file: 
                print(line)

        return fp # sets self.output_file to this value 
    
    '''_________________________________________________________'''
    '''    ------------ Public Methods -------------     '''
     
    def record_event(self, event): 
        # called by monitor_for_event only 
        # gets passed an event from the event_queue that gets written to the output file 
        with open(self.filepath, 'a') as file: 
            round = event[0]
            name = event[1]
            time = event[2]
            # , name, time = event.split(',')
            writer = csv.writer(file, delimiter = ',')
            writer.writerow([round, name, time]) 
            # file.writerow([f'{round}', f'{name}', f'{time}']) 
    
    
    ''' Thread Function '''
    
    def monitor_for_event(self): # for tracking & collecting data 
    # thread that waits for stuff to get added to the event queue and if something is there, it will write to results file.
        
        while True: 
            self.event_lock.acquire()
            event = self.event_queue.get() # if event_queue is empty this will wait for something to be added
            self.event_lock.release()
            # logging.debug('i am monitoring the event queue mmkay')
            self.record_event(event) # function that writes to the output file 
            self.event_queue.task_done()
    
    
    ''' Data Analysis Functions ''' 
         # TODO/LEAVING OFF HERE!! 
         # probably first want to better format how I am writing to the output files cause looks not gr8 rn. 
    def analysis(self): 
        
        print("something will happen here to analyze the data but idg what that is yet. (from resutls.py)")
        # Read In Data 
        df = pd.read_csv(self.filepath, skiprows=1) # does not read the header into the dataframe 
        print(df.head())
        print('-------------------------------')
        self.pellet_latency(df)
    
    
    def pellet_latency(self, df): 
        pellet_df = df.loc[:, 'Event']
        # print(pellet_df.loc['pellet dispensed', 'pellet retrieved'])
        # print(pellet_df.head())
        
    
    ''' Functions to help with Exiting the Program '''          
    def cleanup(self): # finish writing and close file
        with open(self.filepath, 'a') as file: 
            csv.writer(file, delimiter = ',')
            '''while self.event_queue is not Empty: 
                event = self.event_queue.get() 
                file.write(f'({event}) \n')'''
            file.flush()
            file.close()
        return
        
    ''' 
    (TODO)  
        
     
                -create dedicated writer thread (every new instance of ScriptClass should get one)
                -threads or1 and or2, w/ target fn.override_door_1 and fn.override_door_2 
                - to do this, within the __init__ function of Results class, add: 
                    self.writer_thread_id = threading.Thread(target = writeFunction, daemon = True)
                    
        
        def write_results(thread_id, output_file): 
            # write to output_file 
            this function would mimics the fucntion flush_to_CSV that the functions.py file has 
    '''
    '''def write_results(self): 
        # write stuff in the event queue to the output file 
        with open(self.filepath, 'a') as file: # output_file is the new file object 
            csv.writer(file, delimiter = ',')
            
            # https://raspberrypi.stackexchange.com/questions/42867/gpio-wait-for-edge-on-2-channels-at-once
            print('writing results to file rn')
             
            event = self.event_queue.get(timeout=1) # should wait for 
            # self.event_queue.task_done()
                # TODO: event may need formatting before writing to the output file 
            file.write(f'({event}) \n')
            # except Empty: 
            #    print('trying to write results but queue was empty')
            # writer.flush() 
            # writer.close()
            return 
    
     '''
        
    

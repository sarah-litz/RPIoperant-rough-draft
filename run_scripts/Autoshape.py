
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Autoshape.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# Standard Lib Imports 
import time 
import sys 
import traceback 

# Third party imports 
from collections import OrderedDict

# Local imports 
from class_definitions.ScriptClass import Script # import Script # import the parent class 


# ------------------------------------------------------------------------------------
# Autoshape Time Intervals (In Seconds)
# Change these values to adjust the timing of experiment! 

# round_time = 90 # round_time: experiment will complete after exactly 90 seconds 

# wait (?) seconds before extending the lever 
# wait_before_lever_extension = 

# wait (?) seconds to see if the lever gets pressed 
# lever_press_timeout = 
# ------------------------------------------------------------------------------------


# Pin Values: pair a key with a raspberry pi number so we can access a GPIO pin through a descriptive key 
def get_pin_values():  # Pin Values: leave this function as is if default pin values are OK. 
    ''' PIN VALUES DEFINED HERE: if left empty, then default values (from operant_cage_settings_defaults) are used. '''
    pins={} # If diff pin values are desired, then enter values here. 
    return pins 


# Key Values: sets important values that changes the timing/schedule of the script
def get_key_values(): 
    ''' DEFAULT KEY VALUES DEFINED HERE '''
    return OrderedDict([('num_rounds', 20),              # Number of rounds to run Autoshape 
                        ('round_time',90),               # Number of seconds each round should run for 
                        ('timeII',30),                   # Number of seconds lever should wait for vole to press 
                        ('pellet_tone_time',1),          # Number of seconds 'pellet_buzz' will play a sound for 
                        ('pellet_tone_hz',2500),         # Hertz that the 'pellet_buzz' sound will play 
                        ('door_close_tone_time', 1),     # Number of seconds 'door_close_buzz' will play a sound for
                        ('door_close_tone_hz',7000),     # Hertz that the 'door_close_buzz' sound will play
                        ('door_open_tone_time',1),       # Number of seconds 'door_open_buzz' will play a sound for
                        ('door_open_tone_hz',10000),     # Hertz that the 'door_open_buzz' sound will play
                        ('round_start_tone_time',1),     # Number of seconds 'round_buzz' will play a sound for  
                        ('round_start_tone_hz',5000),    # Number of seconds 'round_buzz' will play a sound for   
                        ('delay by day', [0,0,1,1,2]),   # Delay based on what day of experiment it is
                        ('delay default', 2)             # Default delay time
                    ]) 



class Autoshape(Script):    
    def __init__(self, inputdf, inputfp, output_dir, key_values, csv_row_num, pin_obj_dict=None, pin_values=None): 
        super().__init__(inputdf, inputfp, output_dir, key_values, csv_row_num, pin_obj_dict, pin_values)

        print('KEY VALUES ARE: ', self.key_values)
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                           Experiment Variables                            #
        #           change these vals to change order and timing of experiment      #
        #                                                                           # 
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.onPressEvents = [
            lambda: self.pulse_sync_line(length=0.25), 
            lambda: self.buzz(buzz_type='pellet_buzz'),
            lambda: time.sleep(1), 
            lambda: self.dispense_pellet(), 
            lambda: time.sleep(1),         
            lambda: self.pins['lever_food'].retract_lever(), 
        ]

        self.noPressEvents = [
            lambda: self.pulse_sync_line(length=0.25), 
            lambda: self.buzz(buzz_type='pellet_buzz'),
            lambda: time.sleep(1), 
            lambda: self.dispense_pellet(), 
            lambda: time.sleep(1),         
            lambda: self.pins['lever_food'].retract_lever(), 
        ]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



    '''--------- run_script gets called by MainDriver. In charge of instantiating a Script class '''
    def run_script(self):  # csv_input is the row that corresponds with the current script getting run 
        
        results = self.results # make results instance to give output data so it's recorded&analyzed 
        
        results.writer_thread.start() # start up the writer thread to run in background until experiment is over 
        self.executor_manager.start() 
        
        # delay experiment? 
        day_num = 'day' in results.header
        # day_num = int(results.header['day'])
        if day_num > len(self.key_values['delay by day']):
            delay = self.key_values['delay default']
        else:
            delay = self.key_values['delay by day'][day_num-1] 
            
        # make sure all doors are closed
        doors = ['door_1', 'door_2']
        for d in doors:
            if self.doors[d].isOpen() is True:  
                self.doors[d].close_door() 
        
    # dedicate 3 worker threads to monitoring a lever for lever presses thruout 
        levers = ['lever_food', 'lever_door_1', 'lever_door_2']
        for l in levers: # create thread for fulltime monitoring of each lever
            self.pins[l].onPressEvents = self.onPressEvents
            self.pins[l].noPressEvents = self.noPressEvents
            self.executor.submit(self.pins[l].monitor_lever_continuous, self.onPressEvents, self.noPressEvents, callback_func=self.lever_event_callback)
        

        self.executor.submit(self.pulse_sync_line, length=0.5, round = self.round) # Pulse Event: Experiment Start 
        
        '''________________________________________________________________________________________________________________________________________'''
        
        print(f"range for looping: {[i for i in range(1, self.key_values['num_rounds']+1,1)]}")
        
        print(f"setup finished, starting experiment with these key values: \n {self.key_values}: \n")
        for count in range(0, int(self.key_values['num_rounds'])): 

            # ~~ New Round ~~ 
            self.round = count+1
            print("round #",self.round)
            
            # pulse 
            self.thread_pool_submit('new round', self.pulse_sync_line, length=0.1, round = self.round) # Pulse Event: New Round

            # buzz
            self.executor.submit(self.buzz, buzz_type = 'round_buzz') # play sound for round start (type: 'round_buzz')

            # extend food lever
            self.thread_pool_submit('levers out', self.pins['lever_food'].extend_lever)

            # monitoring for lever press 
            self.pins['lever_food'].monitor_lever(press_timeout=self.key_values['timeII'], required_presses=1)                 
            ''',                                        callbacks = [
                                                        lambda: self.pulse_sync_line(round=self.round, length=0.25), # lambda round=script.round, length=0.25: script.pulse_sync_line(round=script.round, length=0.25), 
                                                        lambda: self.buzz(buzz_type='pellet_buzz')
                                                    ])'''
            
            time.sleep(self.key_values['timeII']) # pause for monitoring lever press timeframe  
            # if there is a lever press, the monitor_lever_function automatically pulses/buzzes to indicate this 
            
            # Retract Levers
            self.thread_pool_submit('retracting lever', self.pins['lever_food'].retract_lever)      
            
            time_II_start = time.time() # question: not sure wat this gets used for 
            
            time.sleep(delay) # do not give reward until after delay
            
            # Dispense Pellet in response to Lever Press
            print(f'starting pellet dispensing {self.round}, {time.time() - self.start_time}')
            self.thread_pool_submit('dispense pellet', self.pins['read_pellet'].dispense_pellet)

                    
            # ----- TODO: was pellet retrieved?! --------
            self.thread_pool_submit('pellet retrieval', self.pins['read_pellet'].pellet_retrieval)
            
            # wait on futures to finish running 
            attempts = 0
            print("script futures: ", self.futures)
            while attempts < 5 : 
                for future,name in self.futures: 
                    print(f'(Future Name) {name} (Running) {future.running()}')
                    time.sleep(3)
                attempts += 1
            
            self.round_reset() 

            '''
            # Reset Things before start of next round
            results.event_queue.join() # ensures that all events get written before beginning next round 

            # Update Input CSV file with new rounds completed value 
            self.inputdf.loc[self.csv_row_num,'rounds_completed'] = self.inputdf.loc[self.csv_row_num, 'rounds_completed'] + 1 # update "rounds completed" in input csv file 
            self.inputdf.to_csv(self.inputfp, index=False)
            
            # TODO: reset before next round?? ( reset vals where necessary, shut off servos and stuff )

            if self.round < int(self.key_values['num_rounds']): # skips countdown timer if final round just finished
                self.countdown_timer(self.key_values['round_time'], event='next round')  # countdown until the start of the next round
            else: 
                # Final Round just finished; mark this down in the input csv file by setting the "done" value to True 
                self.inputdf.loc[self.csv_row_num, 'done'] = True 
                self.inputdf.to_csv(self.inputfp, index=False) '''
        
        # TODO: analyze and cleanup
        results.analysis()
        
        return True 


def run(inputdf, inputfp, outputdir, csv_row_num, pin_obj_dict=None): 

    finalClean = False 
    try: 
        key_values = get_key_values()
        pin_values = get_pin_values()
        script = Autoshape(inputdf, inputfp, outputdir, key_values, csv_row_num, pin_obj_dict, pin_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 
        # script.print_pin_status()
        script.run_script()
        
    except KeyboardInterrupt: 
        print(" uh oh interrupt! I will clean up and then exit Autoshape.")
        while True: 
            cont = input("do you want to run the remaining scripts? (y/n)")
            if cont is 'y': 
                return script.pins
            elif cont is 'n': 
                finalClean = True 
                sys.exit(0)
            else: 
                'hmm didnt recognize that input. please only enter y or n'
        
    else: 
        print("Autoshape script has finished running all rounds successfully!")
        return script.pins
    finally: 
        # runs cleanup() no matter what reason there was for exiting 
        try: 
            script.cleanup(finalClean) 
        except UnboundLocalError: 
            traceback.print_tb
            print('~~ Unbound Local Error Caught: got stuck during setup; script never completed setup ~~')
    


    




''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Magazine.py
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



# Pin Values: pair a key with a raspberry pi number so we can access a GPIO pin through a descriptive key 
def get_pin_values():  # Pin Values: leave this function as is if default pin values are OK. 
    ''' PIN VALUES DEFINED HERE: if left empty, then default values (from operant_cage_settings_defaults) are used. '''
    pins={} # If diff pin values are desired, then enter values here. 
    return pins 


# Key Values: sets important values that changes the timing/schedule of the script
def get_key_values(): 
    ''' DEFAULT KEY VALUES DEFINED HERE '''
    return OrderedDict([('num_rounds', 15),         # Number of rounds to run Magazine 
                        ('round_time',90),          # Number of seconds each round should run for 
                        ('timeII',2),               # Number of seconds lever should wait for vole to press 
                        ('timeIV',2),               # Number of seconds to wait after lever press but before retracting lever 
                        ('pellet_tone_time',1),     # Number of seconds 'pellet_buzz' will play a sound for 
                        ('pellet_tone_hz',2500),    # Hertz that the 'pellet_buzz' sound will play
                        ('door_close_tone_hz',7000),# Number of seconds 'door_close_buzz' will play a sound for
                        ('door_open_tone_time',1),  # Number of seconds 'door_open_buzz' will play a sound for 
                        ('door_open_tone_hz',10000),# Hertz that the 'door_open_buzz' sound will play 
                        ('round_start_tone_time',1),# Number of seconds 'round_buzz' will play a sound for  
                        ('round_start_tone_hz',5000)# Hertz that the 'round_buzz' will play a sound for 
                    ]) 


class Magazine(Script): 

    def __init__(self, inputdf, inputfp, output_dir, key_values, csv_row_num, pin_obj_dict=None, pin_values=None): 
        super().__init__(inputdf, inputfp, output_dir, key_values, csv_row_num, pin_obj_dict, pin_values)

        
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


        results = self.results # make results instanceto give output data so it's recorded&analyzed 
        
        results.writer_thread.start() # start up the writer thread to run in background until experiment is over 
        self.executor_manager.start() # start up thread that handles the results that (executor) future objects produce 
        
        #CHANGE1: call to new function: configure callback events 
        # script.configure_callback_events(self.onPressEvents, self.noPressEvents) # set events in case of lever press (or no lever press)
        # make sure all doors are closed
        doors = ['door_1', 'door_2']
        for d in doors:
            print(f'Door State of {d} - isOpen() =', self.doors[d].isOpen())
            print(f'Current Throttle speed of {d} is: {self.doors[d].servo_door.throttle}')
            if self.doors[d].isOpen():  
                self.doors[d].close_door() 
        
        levers = ['lever_food', 'lever_door_1', 'lever_door_2']
        for l in levers: # create thread for fulltime monitoring of each lever
            self.pins[l].onPressEvents = self.onPressEvents
            self.pins[l].noPressEvents = self.noPressEvents
            self.executor.submit(self.pins[l].monitor_lever_continuous, self.onPressEvents, self.noPressEvents, callback_func=self.lever_event_callback)

        self.executor.submit(self.pulse_sync_line, length=0.5, round=self.round) # Pulse Event: Experiment Start 
        
        '''________________________________________________________________________________________________________________________________________'''
        
        print(f"range for looping: {[i for i in range(1, self.key_values['num_rounds']+1,1)]}")
        
        print(f"setup finished, starting experiment with these key values: \n {self.key_values}: \n")
        rounds_completed = int(self.inputdf.loc[self.csv_row_num,'rounds_completed'])
        for count in range(rounds_completed, int(self.key_values['num_rounds'])): 

            # ~~ New Round ~~ 
            self.round = count+1
            print("round #",self.round)

            # pulse 
            self.thread_pool_submit('new round', self.pulse_sync_line, length=0.1, round=self.round) # Pulse Event: New Round
            
            self.executor.submit(self.buzz, 'round_buzz') # play sound for round start (type: 'round_buzz')

            # extend food lever
            self.thread_pool_submit('levers out', self.pins['lever_food'].extend_lever)

            
            # begin monitoring 
            # script.pins['lever_food'].monitor_lever(required_presses=1, press_timeout=script.key_values['timeII'])
            self.pins['lever_food'].monitor_lever(press_timeout=self.key_values['timeII'],  # change back to 'timeII' press timeout value 
                                                    required_presses=1) 
            ''', 
                                                    callbacks = [
                                                        lambda: script.pulse_sync_line(round=script.round, length=0.25), # lambda round=script.round, length=0.25: script.pulse_sync_line(round=script.round, length=0.25), 
                                                        lambda: script.buzz(buzz_type='pellet_buzz')
                                                    ])'''




            time.sleep(self.key_values['timeII']) # pause while we are waiting on lever press 
            
            time_II_start = time.time() # question: not sure wat this gets used for 
    
            # Dispense Pellet in response to Lever Press
            # print(f'starting pellet dispensing {script.round}, {time.time() - script.start_time}')
            # script.thread_pool_submit('dispense pellet', script.pins['read_pellet'].dispense_pellet)


            
            # Retract Levers
            time.sleep(self.key_values['timeIV']) # pause before retracting lever 
            self.thread_pool_submit('retracting lever', self.pins['lever_food'].retract_lever)      

            
            
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

            # Reset Stuff before next round starts
            results.event_queue.join() # ensures that all events get written before beginning next round 
            
            
            # TODO: reset before next round?? ( reset vals where necessary, shut off servos and stuff )
           
            # Update Input CSV file with new rounds completed value 
            print('#', self.inputdf.loc[self.csv_row_num,'rounds_completed'] )
            self.inputdf.loc[self.csv_row_num,'rounds_completed'] = self.inputdf.loc[self.csv_row_num, 'rounds_completed'] + 1 # update "rounds completed" in input csv file 
            print('#', self.inputdf.loc[self.csv_row_num,'rounds_completed'] )
            self.inputdf.to_csv(self.inputfp)
        
            if self.round < int(self.key_values['num_rounds']): # skips countdown timer if final round just finished
                self.countdown_timer(self.key_values['round_time'], event='next round')  # countdown until the start of the next round
            else: 
                # Final Round just finished; mark this down in the input csv file by setting the "done" value to True 
                self.inputdf.loc[self.csv_row_num, 'done'] = True 
                self.inputdf.to_csv(self.inputfp) 
                



        # TODO: analyze and cleanup
        # results.analysis 
        results.analysis() # TODO this should possibly be moved to the end of all rounds for each experiment? 
        # cleanup runs in finally statement (in the run() function)
        return True 


def run(inputdf, inputfp, outputdir, csv_row_num, pin_obj_dict=None): 
    
    # csv_input = csv_input 
    # csv_row = csv_input.loc[csv_row_num]

    # print("CSV INPUT:", csv_input) 
    print("this is only the single row... not the entire input csv path so need to create a way of how we are writing/updating values in the csv file. ")

    finalClean = False 
    try: 
        key_values = get_key_values()
        pin_values = get_pin_values()
        script = Magazine(inputdf, inputfp, outputdir, key_values, csv_row_num, pin_obj_dict, pin_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 

        script.run_script()
        
    except KeyboardInterrupt: 
        print("  uh oh interrupt! I will clean up and then exit Magazine.")
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
        print("Magazine script has finished running all rounds successfully!")
        return script.pins

    finally: 
        # runs cleanup() no matter what reason there was for exiting 

        try: 
            script.cleanup(finalClean) 
        except UnboundLocalError: 
            traceback.print_tb
            print('~~ Unbound Local Error Caught: got stuck during setup; script never completed setup ~~')
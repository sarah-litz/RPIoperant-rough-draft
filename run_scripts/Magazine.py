
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

    def __init__(self, csv_input, output_dir, key_values): 
        super().__init__(csv_input, output_dir, key_values)

        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                           Experiment Variables                            #
        #           change these vals to change order and timing of experiment      #
        #                                                                           # 
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.onPressEvents = [
            lambda: print('Executing the onPressEvents'),
            lambda: self.box.gpio_sync.pulse_sync_line(length=0.25), 
            lambda: self.box.speaker.buzz(    length=self.key_values['pellet_tone_time'], 
                                                hz=self.key_values['pellet_tone_hz'], 
                                                buzz_type='pellet_buzz'),
            lambda: time.sleep(1), 
            lambda: self.box.dispenser.dispense_pellet(), 
            lambda: time.sleep(1),         
            lambda: self.box.food_lever.retract_lever(), 
            lambda: self.box.dispenser.pellet_retrieval(), 
        ]

        self.noPressEvents = [
            lambda: print('Executing the noPressEvents'), 
            lambda: self.box.gpio_sync.pulse_sync_line(length=0.25), 
            lambda: self.box.speaker.buzz(    length=self.key_values['pellet_tone_time'], 
                                                hz=self.key_values['pellet_tone_hz'], 
                                                buzz_type='pellet_buzz'),
            lambda: time.sleep(1), 
            lambda: self.box.dispenser.dispense_pellet(), 
            lambda: time.sleep(self.key_values['timeIV']),         
            lambda: self.box.food_lever.retract_lever(), 
            lambda: self.box.dispenser.pellet_retrieval(), 
        ]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



    
    '''--------- run_script gets called by MainDriver. In charge of instantiating a Script class '''
    def run_script(self):  # csv_input is the row that corresponds with the current script getting run 

        results = self.results # make results instanceto give output data so it's recorded&analyzed 
        box = self.box 

        results.writer_thread.start() # start up the writer thread to run in background until experiment is over 
        self.executor_manager.start() # start up thread that handles the results that (executor) future objects produce 
        
        # make sure all doors are closed
        doors = [box.door_1]
        for door in doors: 
            if door.isOpen(): 
                door.close_door(door.state_button)
        
        # configure onPressEvents and noPressEvents for the levers
        leverlist=[box.food_lever,box.door_1_lever,box.door_2_lever]
        for lever in leverlist: 
            lever.press_timeout = self.key_values['timeII']
            lever.onPressEvents = self.onPressEvents 
            lever.noPressEvents = self.noPressEvents

        self.thread_pool_submit('Experiment Start (Pulse)', box.gpio_sync.pulse_sync_line, length=0.5, descriptor='Experiment Start')
        '''________________________________________________________________________________________________________________________________________'''
        
        print(f"range for looping: {[i for i in range(1, self.key_values['num_rounds']+1,1)]}")
        
        print(f"setup finished, starting experiment with these key values: \n {self.key_values}: \n")
        for count in range(0, int(self.key_values['num_rounds'])): 

            # ~~ New Round ~~ 
            self.new_round() # updates the round num and round start time in the timestamp q
            print("round #",self.round)

            # pulse 
            self.thread_pool_submit('New Round (Pulse)', box.gpio_sync.pulse_sync_line, length=0.1, descriptor=f'New Round (#{self.round})') # Pulse Event: New Round
            
            # buzz
            self.thread_pool_submit('New Round (Buzz)', box.speaker.buzz,  
                                        length=self.key_values['round_start_tone_time'], 
                                        hz=self.key_values['round_start_tone_hz'], 
                                        buzz_type='round_buzz' )

            # extend food lever
            self.thread_pool_submit('levers out', box.food_lever.extend_lever)

            # monitor for a lever press             
            # self.thread_pool_submit('waiting for 2 lever pressees', box.food_lever.wait_for_n_presses, required_presses=2) # diff than syntax in autoshape (just to see what happens)
            box.food_lever.wait_for_n_presses(required_presses=2)

            time.sleep(self.key_values['timeII']) # pause while we are waiting on lever press 
            
            time_II_start = time.time() # question: not sure wat this gets used for 
               

            # TODO: make this wait on futures into a funciton w/in the ScriptClass 
            # wait on futures to finish running 
            attempts = 0
            print("script futures: ", self.futures)
            while attempts < 5 : 
                for future,name in self.futures: 
                    print(f'(Future Name) {name} (Running) {future.running()}')
                    time.sleep(3)
                attempts += 1

            # Reset Stuff before next round starts
            box.timestamp_q.finish_writing_items()             
            

        
            if self.round < int(self.key_values['num_rounds']): # skips countdown timer if final round just finished
                self.countdown_timer(self.key_values['round_time'], event='next round')  # countdown until the start of the next round
        
        # TODO: analyze and cleanup
        # results.analysis 
        # results.analysis() # TODO this should possibly be moved to the end of all rounds for each experiment? 
        # cleanup runs in finally statement (in the run() function)
        return True 


def run(csv_input, output_dir): 
    
    finalClean = False 
    try: 

        key_values = get_key_values()
        script = Magazine(csv_input, output_dir, key_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 

        script.run_script()
        
    except KeyboardInterrupt: 
        print("  uh oh interrupt! I will clean up and then exit Magazine.")
        while True: 
            cont = input("do you want to run the remaining scripts? (y/n)")
            if cont is 'y': 
                return True
            elif cont is 'n': 
                finalClean = True 
                sys.exit(0)
            else: 
                'hmm didnt recognize that input. please only enter y or n'
        
    else: 
        print("Magazine script has finished running all rounds successfully!")
        return True 

    finally: 
        # runs cleanup() no matter what reason there was for exiting 

        try: 
            script.cleanup(finalClean) 
        except UnboundLocalError: 
            traceback.print_tb
            print('~~ Unbound Local Error Caught: got stuck during setup; script never completed setup ~~')
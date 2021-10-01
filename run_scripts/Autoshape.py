
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
    def __init__(self, csv_input, output_dir, key_values): 
        super().__init__(csv_input, output_dir, key_values)

        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                           Experiment Variables                            #
        #           change these vals to change order and timing of experiment      #
        #                                                                           # 
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.onPressEvents = [
            lambda: self.box.gpio_sync.pulse_sync_line(length=0.25), 
            lambda: self.box.speaker.buzz(    length=self.key_values['pellet_tone_time'], 
                                                hz=self.key_values['pellet_tone_hz'], 
                                                buzz_type='pellet_buzz'),
            lambda: time.sleep(1), 
            lambda: self.box.dispenser.dispense_pellet(),
            lambda: self.box.dispenser.pellet_retrieval(),  
            lambda: time.sleep(1),         
            lambda: self.box.food_lever.retract_lever(), 
        ]

        self.noPressEvents = [
            lambda: self.box.gpio_sync.pulse_sync_line(length=0.25), 
            lambda: self.box.speaker.buzz(    length=self.key_values['pellet_tone_time'], 
                                                hz=self.key_values['pellet_tone_hz'], 
                                                buzz_type='pellet_buzz'),
            lambda: time.sleep(1), 
            lambda: self.box.dispenser.dispense_pellet(), 
            lambda: self.box.dispenser.pellet_retrieval(),
            lambda: time.sleep(1),         
            lambda: self.box.food_lever.retract_lever(), 
        ]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



    '''--------- run_script gets called by MainDriver. In charge of instantiating a Script class '''
    def run_script(self):  # csv_input is the row that corresponds with the current script getting run 
        
        results = self.results # make results instance to give output data so it's recorded&analyzed 
        box = self.box 

        results.writer_thread.start() # start up the writer thread to run in background until experiment is over 
        self.executor_manager.start() 
        
        # delay experiment? 
        day_num = 'day' in results.header
        # day_num = int(results.header['day'])
        if day_num > len(self.key_values['delay by day']):
            delay = self.key_values['delay default']
        else:
            delay = self.key_values['delay by day'][day_num-1] 
            
        # make sure all doors are closed: 
            # if door.isOpen(): close_door 

        if box.door_1.isOpen():  # returns True if door is open, False if it is not open aka is closed 
            box.door_1.close_door(box.door_1.state_button) 
        
        # Set the levers' PressEvents defined at the top of this module 
        leverlist=[box.food_lever,box.door_1_lever,box.door_2_lever]
        for lever in leverlist: 
            lever.press_timeout = self.key_values['timeII']
            lever.onPressEvents = self.onPressEvents 
            lever.noPressEvents = self.noPressEvents 

        # self.executor.submit(box.gpio_sync.pulse_sync_line, length=0.5, descriptor='Experiment Start') # Pulse Event: Experiment Start 
        self.thread_pool_submit('Experiment Start (Pulse)', box.gpio_sync.pulse_sync_line, length=0.5, descriptor='Experiment Start')
        '''________________________________________________________________________________________________________________________________________'''
        
        print(f"range for looping: {[i for i in range(1, self.key_values['num_rounds']+1,1)]}")
        
        print(f"setup finished, starting experiment with these key values: \n {self.key_values}: \n")
        for count in range(0, int(self.key_values['num_rounds'])): 

            # ~~ New Round ~~ 
            self.new_round() 
            # self.executor.submit(box.gpio_sync.pulse_sync_line, length=0.5, descriptor=f"New Round (#{self.round})")
            print("round #",self.round)
            
            # pulse 
            self.thread_pool_submit('New Round (Pulse)', box.gpio_sync.pulse_sync_line, length=0.1, descriptor=f'New Round (#{self.round})') # Pulse Event: New Round

            # buzz
            # self.executor.submit(box.speaker, buzz_type = 'round_buzz') # play sound for round start (type: 'round_buzz')
            self.thread_pool_submit('New Round (Buzz)', box.speaker.buzz,  
                                        length=self.key_values['round_start_tone_time'], 
                                        hz=self.key_values['round_start_tone_hz'], 
                                        buzz_type='round_buzz' )
            # extend food lever
            self.thread_pool_submit('levers out', box.food_lever.extend_lever)

            # monitoring for lever press 
            # box.food_lever.monitor_lever(press_timeout=self.key_values['timeII'], required_presses=1)                 
            box.food_lever.wait_for_n_presses(required_presses=2)
            
            time.sleep(self.key_values['timeII']) # pause for monitoring lever press timeframe  
            # if there is a lever press, the monitor_lever_function automatically pulses/buzzes to indicate this 
            
            # Retract Levers
            # self.thread_pool_submit('retracting lever', box.food_lever.retract_lever)      
            
            time_II_start = time.time() # question: not sure wat this gets used for 
            
            time.sleep(delay) # do not give reward until after delay
            
            # Dispense Pellet in response to Lever Press
            # print(f'starting pellet dispensing {self.round}, {time.time() - self.start_time}')
            # self.thread_pool_submit('dispense pellet', box.dispenser.dispense_pellet)

                    
            # ----- TODO: was pellet retrieved?! --------
            self.thread_pool_submit('pellet retrieval', box.dispenser.pellet_retrieval)
            
            # wait on futures to finish running 
            attempts = 0
            print("script futures: ", self.futures)
            while attempts < 5 : 
                for future,name in self.futures: 
                    print(f'(func name){name} (running){future.running()}')
                    time.sleep(3)
                attempts += 1
            
            
            # Reset Things before start of next round
            box.timestamp_q.finish_writing_items() # ensures that all events get written before beginning next round 
            # results.event_queue.join() # ensures that all events get written before beginning next round 
            
            # TODO: reset before next round?? ( reset vals where necessary, shut off servos and stuff )
            # results.analysis() # TODO this should possibly be moved to the end of all rounds for each experiment? 
        
            if self.round < int(self.key_values['num_rounds']): # skips countdown timer if final round just finished
                self.countdown_timer(self.key_values['round_time'], event='next round')  # countdown until the start of the next round        
        
        # TODO: analyze and cleanup
        # results.analysis 
        
        return True 


def run(csv_input, output_dir): 

    finalClean = False 
    try: 
        key_values = get_key_values()
        script = Autoshape(csv_input, output_dir, key_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 
        # script.print_pin_status()
        script.run_script()
        
    except KeyboardInterrupt: 
        print(" uh oh interrupt! I will clean up and then exit Autoshape.")
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
        print("Autoshape script has finished running all rounds successfully!")
        return True 
    finally: 
        # runs cleanup() no matter what reason there was for exiting 
        try: 
            script.cleanup(finalClean) 
        except UnboundLocalError: 
            traceback.print_tb
            print('~~ Unbound Local Error Caught: got stuck during setup; script never completed setup ~~')
    


    



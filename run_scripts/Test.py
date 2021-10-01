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

class Test(Script): 
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


    def run_script(self):  # csv_input is the row that corresponds with the current script getting run 

        box = self.box 

        result = box.dispenser.dispense_pellet() 

        print(result)

        pin_lst = [box.dispenser.pin, box.food_lever.pin, box.door_1.open_override.pin, box.door_1.close_override.pin]
        self.print_pin_status(pin_lst)
        return 
    


def run(csv_input, output_dir): 
    
    finalClean = False 
    try: 

        key_values = get_key_values()
        script = Test(csv_input, output_dir, key_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 

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
        print("Test script has finished running all rounds successfully!")
        return True 

    finally: 
        # runs cleanup() no matter what reason there was for exiting 

        try: 
            script.cleanup(finalClean) 
        except UnboundLocalError: 
            traceback.print_tb
            print('~~ Unbound Local Error Caught: got stuck during setup; script never completed setup ~~')

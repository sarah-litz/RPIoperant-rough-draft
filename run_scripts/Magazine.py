
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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                                             #
#                            Experiment Variables                                             #
#                   ( change these values, do not change variable names)                      #       
#                                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



onPressEvents = [
    'script.pulse_sync_line(length=0.25)', 
    "script.buzz(buzz_type='pellet_buzz')",
    'time.sleep(1)', 
    'script.dispense_pellet()', 
    'time.sleep(1)',         
    "script.pins['lever_food'].retract_lever()", 
]

noPressEvents = [
    'script.pulse_sync_line(length=0.25)', 
    "script.buzz(buzz_type='pellet_buzz')", 
    'time.sleep(1)', 
    'script.dispense_pellet()', 
    'time.sleep(1)',         
    "script.pins['lever_food'].retract_lever()", 
]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


''' ~ ~ ~ functions for getting default values! ~ ~ ~ ''' 
      #  Defined Here: values for pins and key values 
        
def get_pin_values():  # TODO: possibly delete this function
    ''' PIN VALUES DEFINED HERE: if left empty, then default values (from operant_cage_settings_defaults) are used. '''
    pins={}
    return pins 

def get_key_values(): 
    ''' DEFAULT KEY VALUES DEFINED HERE '''
    return OrderedDict([('num_rounds', 15), ('round_time',90), 
                                        ('timeII',2), ('timeIV',2), 
                                        ('pellet_tone_time',1), ('pellet_tone_hz',2500), 
                                        ('door_close_tone_hz',7000), ('door_open_tone_time',1), ('door_open_tone_hz',10000),
                                        ('round_start_tone_time',1), ('round_start_tone_hz',5000)
                                    ]) 


        
'''--------- run_script gets called by MainDriver. In charge of instantiating a Script class '''
def run_script(script):  # csv_input is the row that corresponds with the current script getting run 


    results = script.results # make results instanceto give output data so it's recorded&analyzed 
    
    results.writer_thread.start() # start up the writer thread to run in background until experiment is over 
    script.executor_manager.start() # start up thread that handles the results that (executor) future objects produce 
    
    #CHANGE1: call to new function: configure callback events 
    script.configure_callback_events(onPressEvents, noPressEvents) # set events in case of lever press (or no lever press)
    # make sure all doors are closed
    doors = ['door_1', 'door_2']
    for d in doors:
        print(f'Door State of {d} - isOpen() =', script.doors[d].isOpen())
        print(f'Current Throttle speed of {d} is: {script.doors[d].servo_door.throttle}')
        if script.doors[d].isOpen():  
            script.doors[d].close_door() 
    
    levers = ['lever_food', 'lever_door_1', 'lever_door_2']
    for l in levers: # create thread for fulltime monitoring of each lever
        script.pins[l].onPressEvents = script.onPressEvents
        script.pins[l].noPressEvents = script.noPressEvents
        script.executor.submit(script.pins[l].monitor_lever_continuous, script.onPressEvents, script.noPressEvents, callback_func=script.lever_event_callback)

    script.executor.submit(script.pulse_sync_line, length=0.5, round=script.round) # Pulse Event: Experiment Start 
       
    '''________________________________________________________________________________________________________________________________________'''
    
    print(f"range for looping: {[i for i in range(1, script.key_values['num_rounds']+1,1)]}")
    
    print(f"setup finished, starting experiment with these key values: \n {script.key_values}: \n")
    for count in range(0, int(script.key_values['num_rounds'])): 

        # ~~ New Round ~~ 
        script.round = count+1
        print("round #",script.round)

        # pulse 
        script.thread_pool_submit('new round', script.pulse_sync_line, length=0.1, round=script.round) # Pulse Event: New Round
        
        script.executor.submit(script.buzz, 'round_buzz') # play sound for round start (type: 'round_buzz')

        # extend food lever
        script.thread_pool_submit('levers out', script.pins['lever_food'].extend_lever)

        
        # begin monitoring 
        # script.pins['lever_food'].monitor_lever(required_presses=1, press_timeout=script.key_values['timeII'])
        script.pins['lever_food'].monitor_lever(press_timeout=script.key_values['timeII'],  # change back to 'timeII' press timeout value 
                                                required_presses=1) 
        ''', 
                                                callbacks = [
                                                    lambda: script.pulse_sync_line(round=script.round, length=0.25), # lambda round=script.round, length=0.25: script.pulse_sync_line(round=script.round, length=0.25), 
                                                    lambda: script.buzz(buzz_type='pellet_buzz')
                                                ])'''




        time.sleep(script.key_values['timeII']) # pause while we are waiting on lever press 
        
        time_II_start = time.time() # question: not sure wat this gets used for 
   
        # Dispense Pellet in response to Lever Press
        # print(f'starting pellet dispensing {script.round}, {time.time() - script.start_time}')
        # script.thread_pool_submit('dispense pellet', script.pins['read_pellet'].dispense_pellet)


        
        # Retract Levers
        time.sleep(script.key_values['timeIV']) # pause before retracting lever 
        script.thread_pool_submit('retracting lever', script.pins['lever_food'].retract_lever)      

        
        
        # ----- TODO: was pellet retrieved?! --------
        script.thread_pool_submit('pellet retrieval', script.pins['read_pellet'].pellet_retrieval)

        
       
        # wait on futures to finish running 
        attempts = 0
        print("script futures: ", script.futures)
        while attempts < 5 : 
            for future,name in script.futures: 
                print(f'(Future Name) {name} (Running) {future.running()}')
                time.sleep(3)
            attempts += 1

        # Reset Stuff before next round starts
        results.event_queue.join() # ensures that all events get written before beginning next round 
         
        
        # TODO: reset before next round?? ( reset vals where necessary, shut off servos and stuff )

       
        if script.round < int(script.key_values['num_rounds']): # skips countdown timer if final round just finished
            script.countdown_timer(script.key_values['round_time'], event='next round')  # countdown until the start of the next round
    
    # TODO: analyze and cleanup
    # results.analysis 
    results.analysis() # TODO this should possibly be moved to the end of all rounds for each experiment? 
    # cleanup runs in finally statement (in the run() function)
    return True 


def run(csv_input, output_dir, pin_obj_dict=None): 
    
    finalClean = False 
    try: 
 
        key_values = get_key_values()
        pin_values = get_pin_values()
        script = Script(csv_input, output_dir, key_values, pin_obj_dict, pin_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 
        
        # script.print_pin_status()
        run_script(script) 
        
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


    



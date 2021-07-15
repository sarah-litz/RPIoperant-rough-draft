
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Autoshape.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# Standard Lib Imports 
import time 
import sys 

# Third party imports 
from collections import OrderedDict

# Local imports 
from class_definitions.ScriptClass import Script # import Script # import the parent class 


''' ~ ~ ~ functions for getting default values! ~ ~ ~ ''' 
      #  Defined Here: values for pins and key values 
        
def get_pin_values():  # TODO: possibly delete this function
    ''' PIN VALUES DEFINED HERE: if left empty, then default values (from operant_cage_settings_defaults) are used. '''
    pins={}
    return pins 

def get_key_values(): 
    ''' DEFAULT KEY VALUES DEFINED HERE '''
    return OrderedDict([('num_rounds', 20), ('round_time',90), 
                                        ('timeII',30), 
                                        ('pellet_tone_time',1), ('pellet_tone_hz',2500), 
                                        ('door_close_tone_time', 1), ('door_close_tone_hz',7000), ('door_open_tone_time',1), ('door_open_tone_hz',10000),
                                        ('round_start_tone_time',1), ('round_start_tone_hz',5000), 
                                        ('delay by day', [0,0,1,1,2]), ('delay default', 2)
                                    ]) 


        
'''--------- run_script gets called by MainDriver. In charge of instantiating a Script class '''
def run_script(script):  # csv_input is the row that corresponds with the current script getting run 
    
    results = script.results # make results instanceto give output data so it's recorded&analyzed 
    
    results.writer_thread.start() # start up the writer thread to run in background until experiment is over 
    script.executor_manager.start() 
    
    # delay experiment? 
    day_num = 'day' in results.header
    # day_num = int(results.header['day'])
    if day_num > len(script.key_values['delay by day']):
        delay = script.key_values['delay default']
    else:
        delay = script.key_values['delay by day'][day_num-1] 
        
    # make sure all doors are closed
    doors = ['door_1', 'door_2']
    for d in doors:
        if script.doors[d].isOpen() is True:  
            script.doors[d].close_door() 
    
   # dedicate 3 worker threads to monitoring a lever for lever presses thruout 
    levers = ['lever_food', 'lever_door_1', 'lever_door_2']
    for l in levers: # create thread for fulltime monitoring of each lever
        script.executor.submit(script.pins[l].monitor_lever_continuous, callback_func=script.lever_event_callback)
    

    script.executor.submit(script.pulse_sync_line, script.round, length=0.5) # Pulse Event: Experiment Start 
       
    '''________________________________________________________________________________________________________________________________________'''
    
    print(f"range for looping: {[i for i in range(1, script.key_values['num_rounds']+1,1)]}")
    
    print(f"setup finished, starting experiment with these key values: \n {script.key_values}: \n")
    for count in range(0, int(script.key_values['num_rounds'])): 

        # ~~ New Round ~~ 
        script.round = count+1
        print("round #",script.round)
        
        script.executor.submit(script.pulse_sync_line, script.round, length=0.1) # Pulse Event: New Round 
        results.event_queue.put([script.round, 'new round', time.time()-script.start_time]) # add to timestamp_queue aka event_queue 
        script.executor.submit(script.buzz, 'round_buzz') # play sound for round start (type: 'round_buzz')

        # extend food lever
        future_extend = script.executor.submit(script.pins['lever_food'].extend_lever) 
        script.futures.append(future_extend)

        # monitoring for lever press 
        script.pins['lever_food'].required_presses = 1 # set the number of presses that vole must perform to trigger reward
        script.pins['lever_food'].press_timeout = script.key_values['timeII'] # num of seconds vole has to press lever 
        script.pins['lever_food'].monitoring=True # signals the Lever Monitoring Thread that we are now in timeframe where we want vole to make a lever press. 
        time.sleep(script.pins['lever_food'].press_timeout) # pause for monitoring lever press timeframe  
        # if there is a lever press, the monitor_lever_function automatically pulses/buzzes to indicate this 
        
        # Retract Levers
        future_retract = script.executor.submit(script.pins['lever_food'].retract_lever) 
        script.futures.append(future_retract)                 
        
        time_II_start = time.time() # question: not sure wat this gets used for 
        
        # Dispense Pellet in response to Lever Press
        print(f'starting pellet dispensing {script.round}, {time.time() - script.start_time}')
        future_dispense = script.executor.submit(script.pins['read_pellet'].dispense_pellet)
        script.futures.append(future_dispense)

                
        # ----- TODO: was pellet retrieved?! --------
        future_retrieval = script.executor.submit(script.pins['read_pellet'].pellet_retrieval)
        script.futures.append(future_retrieval)
        
        # wait on futures to finish running 
        attempts = 0
        while len(script.futures) > 0: 
            attempts += 1 
            for f in script.futures: 
                print(f'(Future) {f} (Running) {f.running()}')
            if attempts > 5:  break 
            else: time.sleep(3)
        
        # Reset Things before start of next round
        results.event_queue.join() # ensures that all events get written before beginning next round 

        
        # TODO: reset before next round?? ( reset vals where necessary, shut off servos and stuff )
        results.analysis() # TODO this should possibly be moved to the end of all rounds for each experiment? 
       
        script.countdown_timer(script.key_values['round_time'], event='next round')  # countdown until the start of the next round
    
    # TODO: analyze and cleanup
    # results.analysis 
    
    return True 


def run(csv_input, output_dir): 
    try: 
 
        key_values = get_key_values()
        pin_values = get_pin_values()
        script = Script(csv_input, output_dir, key_values, pin_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 
        # script.print_pin_status()
        run_script(script) 
        
    except KeyboardInterrupt: 
        print("  uh oh interrupt! I will clean up and then exit Autoshape.")
        script.cleanup() 
        while True: 
            cont = input("do you want to run the remaining scripts? (y/n)")
            if cont is 'y': 
                return 
            elif cont is 'n': 
                sys.exit(0) # ends program immediately 
            else: 
                'hmm didnt recognize that input. please only enter y or n'
        
    else: 
        print("Magazine script has finished running all rounds successfully!")
        script.cleanup()
        # TODO: any extra cleanup stuff if needed?? 
        
    


    



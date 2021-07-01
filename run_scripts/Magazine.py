
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Magazine.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# Standard Lib Imports 
import time 

# Third party imports 
from collections import OrderedDict

# Local imports 
from class_definitions.ScriptClass import Script # import Script # import the parent class 


''' ~ ~ ~ functions for getting default values! ~ ~ ~ ''' 
      #  Defined Here: values for pins and key values 
        
def get_pin_values():  # TODO: possibly delete this function
    ''' PIN VALUES DEFINED HERE: if left empty, then default values (from operant_cage_settings_defaults) are used. '''
    pins = {}
    return pins 

def get_key_values(): 
    ''' DEFAUTL KEY VALUES DEFINED HERE '''
    return OrderedDict([('num_rounds', 15), ('round_time',90), 
                                        ('timeII',2), ('timeIV',2), 
                                        ('pellet_tone_time',1), ('pellet_tone_hz',2500), 
                                        ('door_close_tone_hz',7000), ('door_open_tone_time',1), ('door_open_tone_hz',10000),
                                        ('round_start_tone_time',1), ('round_start_tone_hz',5000)
                                    ]) 


'''--------- run_script gets called by MainDriver. In charge of instantiating a Script class '''
def run_script(script):  # csv_input is the row that corresponds with the current script getting run 
 

    results = script.results
    
    results.writer_thread.start() # start up the writer thread to run in background until experiment is over 
    
    # script.start_time = time.time() # start timing 
    
    # make sure all doors are closed
    doors = ['door_1', 'door_2']
    for d in doors:
        if script.doors[d].isOpen() is True:  
            script.doors[d].close_door() 
       
     
    # pulse to signify start of experiment 
    script.pins['gpio_sync'].pulse_sync_line(length=0.5) # Event: Experiment Start
       
    '''________________________________________________________________________________________________________________________________________'''
    
    print(f"range for looping: {[i for i in range(1, script.key_values['num_rounds']+1,1)]}")
    
    print(f"setup finished, starting experiment with these key values: \n {script.key_values}: \n")
    for count in range(0, int(script.key_values['num_rounds'])): 

        # ~~ New Round ~~ 
        round_start = time.time()
        script.round = count+1
        print("round #",script.round)
        script.pulse_sync_line(length=0.1) # Pulse for Event: New Round Start
        
        results.event_queue.put([script.round, 'new round', round_start-script.start_time]) # add to timestamp_queue aka event_queue 
        script.buzz('round_buzz') # play sound for round start (type: 'round_buzz')

    
        # extend and monitor for presses on food lever 
        script.pins['lever_food'].extend_lever()
        
        timeout = script.key_values['timeII'] # timeout value for lever press detection
        event, timestamp = script.pins['lever_food'].detect_event(timeout)
        
        time_II_start = time.time() # question: not sure wat this gets used for 

        if event: # wait until an event is detected on the lever_food pin or the timeout is reached
            # lever was pressed
            script.pulse_sync_line(length=0.25) # Pulse for Event: Lever Press 
            script.buzz('pellet_buzz') # play sound for lever press  
            results.event_queue.put([script.round, 'lever_food pressed', timestamp-script.start_time]) # record event in event queue
            # TODO: dispense pellet             
        else: # else, timed out meaning vole did not press lever    
            script.buzz('pellet_buzz') # play sound 
            # TODO: dispense pellet anyways
            print('no press detected')
        
        print(f'starting pellet dispensing {script.round}, {time.time() - script.start_time}')
        event, pellet_dispensed_timestamp = script.pins['read_pellet'].dispense_pellet()
        
        time.sleep(script.key_values['timeIV']) # pause before retracting lever 
                
        script.pins['lever_food'].retract_lever()
        
        # TODO: check to see if pellet was retrieved (pellet_state)
        if event: # pellet was dispensed 
            results.event_queue.put([script.round, 'pellet dispensed', pellet_dispensed_timestamp-script.start_time])
        else:  # pellet was not dispensed 
            results.event_queue.put([script.round, 'pellet dispense failure', pellet_dispensed_timestamp-script.start_time])
            
        # TODO: wait for writer thread to finish writing
        results.event_queue.join() # ensures that all events get written before beginning next round 
        # TODO: cleanup before next round?? ( reset vals where necessary, shut off servos and stuff )
        # ~~ end of for loop for looping thru specified number of rounds ~~ 
        results.analysis()
        # countdown until the start of the next round: 
        script.countdown_timer(script.key_values['round_time'], event='next round') 
    # TODO: analyze and cleanup
    # results.analysis 
    
    return True 


def run(csv_input, output_dir): 
    try: 
 
        key_values = get_key_values()
        script = Script(csv_input, output_dir, key_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 
        run_script(script) 
        
    except KeyboardInterrupt: 
        print("  uh oh interrupt! I will clean up and then exit Magazine.")
        script.cleanup() 
        
    


    



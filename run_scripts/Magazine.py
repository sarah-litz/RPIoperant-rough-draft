
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


# class Magazine(Script)  

''' ~ ~ ~ functions for getting default values! ~ ~ ~  
        Defined Here: values for pins and key values '''
        
def get_pin_values(): 
    ''' PIN VALUES DEFINED HERE: if left empty, then default values (from operant_cage_settings_defaults) are used. '''
    pins = {}
    return pins 

def get_key_values(): 
    # not defined inside of Magazine class for more accessibility when testing individual scripts 
    ''' DEFAUTL KEY VALUES DEFINED HERE '''
    return OrderedDict([('num_rounds', 15), ('round_time',90), 
                                        ('timeII',2), ('timeIV',2), 
                                        ('pellet_tone_time',1), ('pellet_tone_hz',2500), 
                                        ('door_close_tone_hz',7000), ('door_open_tone_time',1), ('door_open_tone_hz',10000),
                                        ('round_start_tone_time',1), ('round_start_tone_hz',5000)
                                    ]) 


'''--------- run_script gets called by MainDriver. In charge of instantiating a Script class '''
def run_script(csv_input, output_dir):  # csv_input is the row that corresponds with the current script getting run 
 
    key_values = get_key_values()
    magazine = Script(csv_input, output_dir, key_values) # to change pin values, add values to the function get_pin_values, and then pass get_pin_values() as another argument to Script class. 
    
    magazine.pins['gpio_sync'].pulse_sync_line(length=0.5) # Event: Experiment Start
    
    # TODO/QUESTION on my close_door() function in general. This includes the calling process here, as well as the actual function
    # close all doors 
    door_pins = magazine.get_pins_of_type('Door') # get list of the door pins 
    # TODO/QUESTION: confused on what the diff pins of "door" type do... Is it incorrect to pass all of them to the close_door function?? 
    '''for p in door_pins: 
        print("Closing:", p.key)
        p.close_door() # close all doors'''
    # QUESTION(cont) here is the other version where I only close lever_door_1 and lever_door_2 
    print("Closing lever_door_1 and lever_door_2")
    magazine.pins['lever_door_1'].close_door()
    magazine.pins['lever_door_2'].close_door()
    
    
    print(f"range for looping: {[i for i in range(1, key_values['num_rounds']+1,1)]}")

    # round start buzz 
    
    
    print(f"setup finished, starting experiment with these key values: \n {magazine.key_values}: \n")
    for count in range(0, int(magazine.key_values['num_rounds'])): 

        round_start = time.time()
        print("round #",count+1)
        
        magazine.pins['lever_food'].extend_lever()
        # function: monitor lever 
        
        time_II_start = time.time()
        
        # wait for press
        timeout = magazine.key_values['timeII'] # timeout value for lever press detection
        # callback = ??? 
        if magazine.pins['lever_food'].detect_event(timeout) is True: # wait until an event is detected on the lever_food pin or the timeout is reached
            # lever was pressed
            # dispense pellet
            pass  
        else: # else, timed out meaning vole did not press lever
            # dispense pellet anyways
            pass
        
        time.sleep(magazine.key_values['timeIV']) # pause before retracting lever 
        
        # TODO/QUESTION: 
        # pulse sync line?? 
        # lever_press_queue ?? 
        
        magazine.pins['lever_food'].retract_lever()
        
        # countdown until the start of the next round: 
        magazine.countdown_timer(magazine.key_values['round_time'], event='next round')
       
        

    return True 
    



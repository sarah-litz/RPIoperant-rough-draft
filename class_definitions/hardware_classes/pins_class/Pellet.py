''' ----------------------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Pellet.py
                            description: Subclass of Pins. Pellet objects are instantiated during pin_setup() in ScriptClass.py
                            at the moment there is only one pin that is of type "Pellet", and that is the pin 'read_pellet'. 
                            Pellet Class contains functions that only apply to Pellets including functions that work together to 
                            dispense a pellet and track if that pellet gets retrieved from the trough. 
-------------------------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

#standard lib imports 
import time 

# third party imports 
import RPi.GPIO as GPIO

# local imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.Pin import Pin


class Pellet(Pin): 
    # contains attributes and methods that are specific to dispensing a pellet 
    # only the pin 'read_pellet' is made as type Pellet 
    # CONTROLLED BY SERVOS ( accessed thru servo_dict in original code )

    def __init__(self, pin_name, pin_number): 
        super().__init__(pin_name, pin_number)
        # pin of this type will always be the 'read_pellet' pin. 
        self.servo_pellet = default_operant_settings.servo_dict['dispense_pellet']
        self.continuous_servo_speeds = default_operant_settings.continuous_servo_speeds['dispense_pellet']
        self.type = 'Pellet'
        # attributes for tracking the current state of the pellet
        # self.pellet_exists = False # True if pellet is there, False if no pellet 
    
    def troughEmpty(self): 
        # returns True if pellet is in trough, False if it is not 
        return GPIO.input(self.number) # checks the 'read_pellet' pin 
    
    def pellet_retrieval(self): # watches for pellet retrieval 
        # called on the 'read_pellet' pin 
        'Monitoring for pellet retrieval...'
        if self.troughEmpty(): 
            print('there is no pellet in trough, so it is pointless to monitor for pellet_retrieval so returning from this function now!')
            return False, time.time()
        
        time_start = time.time()
        empty_count = 0 # counts number of times that the pin reads the trough as being empty 
        pelletExists_count = 0 # counts the number of times that the pin reads the trough as containing a pellet 
        
        while time.time() - time_start < 2000: 
            if self.troughEmpty(): 
                # nothing is in the trough 
                empty_count += 1
            else: 
                pelletExists_count += 1
            
            if pelletExists_count > 3: 
                # at this point we will assume that any empty reads that the sensor read were a mistake, so starting over from 0 
                empty_count = 0
                pelletExists_count = 0 
                
            if empty_count > 5: 
                print("pellet retrieved!")
                return True, time.time()
            
            else: 
                time.sleep(0.025)

            return False, time.time()
          
        
    def dispense_pellet(self): 
        
        if not self.troughEmpty(): # there is already a pellet, do not dispense
            return False, time.time()   
        else: # dispense pellet 
            
           # QUESTION: confused on some aspects of the original dispense_pellet function that is written. 
            # TODO: pause to prevent confusing vole pressing the trough w/ actual pellet getting dispensed 
            print('SERVO FOR THE PELLET IS: ', self.servo_pellet)
            self.servo_pellet.throttle = self.continuous_servo_speeds['fwd'] # start moving servo 
            print('SERVO SPEED FOR THE PELLET IS: ', self.continuous_servo_speeds['fwd'])
            event, event_timestamp = self.detect_event(timeout=3, edge=GPIO.FALLING) 
            self.continuous_servo_speeds['stop']
            if event: 
                # a pellet was dispensed  
                return event, event_timestamp 
            else: 
                # timed out, pellet did not get dispensed.
                return event, event_timestamp  
            
            '''timeout = False; start_time = time.time()
            while timeout is False: 
                if not GPIO.input(self.number): 
                    # pellet has been dispensed in trough 
                    self.servo_pellet.throttle = self.continuous_servo_speeds['stop']
                    self.pellet_exists = True 
                    return True 
                if (time.time() > start_time+3): # if 3 seconds have passed
                    return False'''  
                    
    def cleanup(self): 
        pass 
                    
                
                
                  
                 
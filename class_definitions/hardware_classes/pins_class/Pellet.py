
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
        
        # attributes for tracking the current state of the pellet
        self.pellet_exists = False # True if pellet is there, False if no pellet 
    
    def dispense_pellet(self): 
        
        if self.pellet_exists: # there is already a pellet, do not dispense
            return None  
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
                self.pellet_exists = True 
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
                    
                
                
                  
                 
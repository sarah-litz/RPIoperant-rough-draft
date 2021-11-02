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


class Pellet(): 
    # contains attributes and methods that are specific to dispensing a pellet 
    # only the pin 'read_pellet' is made as type Pellet 
    # CONTROLLED BY SERVOS ( accessed thru servo_dict in original code )

    def __init__(self, dispenser_dict, timestamp_manager): 
        #super().__init__(dispenser_dict['name'], dispenser_dict['pin']) # passes the pin name and pin number 
        
        self.pin = dispenser_dict['pin']
        self._gpio_setup_pin()

        self.timestamp_manager = timestamp_manager
        self.name = dispenser_dict['name']

        self.servo = dispenser_dict['servo']
        self.stop_speed = dispenser_dict['stop']
        self.forward_speed = dispenser_dict['forward']
        self.timeout = dispenser_dict['timeout']


    
    def _gpio_setup_pin(self): 
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)

    def troughEmpty(self): 
        # returns True if pellet is in trough, False if it is not 
        # print("Dispenser Pin Number:", self.pin)
        # print ('TROUGH EMPTY VALUE: ')
        # print (GPIO.input(self.pin))
        return GPIO.input(self.pin) # checks the 'read_pellet' pin 
    
    def pellet_retrieval(self): # watches for pellet retrieval 
        # called on the 'read_pellet' pin 
        'Monitoring for pellet retrieval...'
        if self.troughEmpty(): 
            print('there is no pellet in trough, so it is pointless to monitor for pellet_retrieval so returning from this function now!')
            return 'no pellet in trough to retrieve', time.time(), False
        
        time_start = time.time()
        empty_count = 0 # counts number of times that the pin reads the trough as being empty 
        pelletExists_count = 0 # counts the number of times that the pin reads the trough as containing a pellet 
        
        while time.time() - time_start < 2: 
            # print("TIME: ", time.time() - time_start)
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
                return 'pellet retrieved', time.time(), True
            
            else: 
                time.sleep(0.025)

        print("troughEmpty:", self.troughEmpty())
        return 'pellet not retrieved', time.time(), False
          
        
    def dispense_pellet(self): 
        
        if not self.troughEmpty(): # there is already a pellet, do not dispense
            self.timestamp_manager.put_item(timestamp=time.time(), event_descriptor='Skipped Pellet Dispense; Trough Not Empty')
            return 'pellet already in trough; skipped dispense', time.time(), False   
        else: # dispense pellet 
            
           # QUESTION: confused on some aspects of the original dispense_pellet function that is written. 
            # TODO: pause to prevent confusing vole pressing the trough w/ actual pellet getting dispensed 
            print('SERVO FOR THE PELLET IS: ', self.servo_pellet)
            self.servo_pellet.throttle = self.continuous_servo_speeds['fwd'] # start moving servo 
            print('SERVO SPEED FOR THE PELLET IS: ', self.continuous_servo_speeds['fwd'])
            # event_bool, event_timestamp = self.detect_event(timeout=3, edge=GPIO.FALLING) 
            channel = GPIO.wait_for_edge(self.pin, GPIO.FALLING, timeout=3000, bouncetime=200)
            self.servo_pellet.throttle = self.continuous_servo_speeds['stop'] # stop moving servo 
            if channel: 
                # a pellet was dispensed  
                self.timestamp_manager.put_item(timestamp=time.time(), event_descriptor='Pellet Dispensed')
                return True 
            else: 
                # timed out, pellet did not get dispensed.
                self.timestamp_manager.put_item(timestamp=time.time(), event_descriptor='Pellet Dispense Failure')
                return False 
            
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
                    
                
                
                  
                 

#!/usr/bin/python3

# Local Imports 
from ...Timestamp import Timestamp 

# standard lib imports 
import time 

# third party imports 
import RPi.GPIO as GPIO


class Button(): 
    def __init__(self, button_dict, timestamp_manager): 

        self.timestamp_manager = timestamp_manager 
        
        self.door = button_dict['name']
        self.function = button_dict['function']
        self.name = button_dict['name']

        self.pin = button_dict['pin']
        self._gpio_setup_pin()

        self.stop_threads = False  
        self.flag = False # flag to notify the calling process that a button was pressed  

    def _gpio_setup_pin(self): 
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    

    def monitor_for_button_press(self): 
        print('______________Monitoring for Button Press___________________________')
        
        self.flag = False 
        GPIO.add_event_detect(self.pin, GPIO.FALLING, bouncetime=200)
        while True: 
            if GPIO.event_detected(self.pin): 
                print('override button press detected!!')
                ## Since this is continuously looping for all of the buttons not sure best way to make sure a new Timestamp is created each press?? 
                # Cause need to make sure round/phase/things get updated if we are just continuously looping. 
                # This one might be the exception of we just want to create the timestamp and add it to queue all at the same time 
                Timestamp(self.timestamp_manager, f'override {self.function} button for {self.door} pressed', time.time()).add_to_queue() 
                self.flag = True   

            if self.stop_threads is True: 
                GPIO.remove_event_detect(self.pin)
                return 

    def stop_monitoring(self): 
        self.stop_threads = True   

    def cleanup(self): 
        pass 





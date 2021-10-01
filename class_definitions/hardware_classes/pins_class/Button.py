
#!/usr/bin/python3

# standard lib imports 
import time 

# third party imports 
import RPi.GPIO as GPIO


class Button(): 
    def __init__(self, button_dict, timestamp_q): 

        self.timestamp_q = timestamp_q 
        
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
                self.timestamp_q.put_item(time.time(), f'override {self.function} button for {self.door} pressed')
                self.flag = True   

            if self.stop_threads is True: 
                GPIO.remove_event_detect(self.pin)
                return 

    def stop_monitoring(self): 
        self.stop_threads = True   

    def cleanup(self): 
        pass 





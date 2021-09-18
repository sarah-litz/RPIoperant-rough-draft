
#!/usr/bin/python3


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

    def _gpio_setup_pin(self): 
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    

    def monitor_for_button_press(self, button_press_flag): 
        
        button_press_flag = False 
        GPIO.add_event_detect(self.pin, GPIO.FALLING, bouncetime=200)
        while True: 
            if GPIO.event_detected(self.pin): 
                button_press_flag = True   

    def cleanup(self): 
        pass 




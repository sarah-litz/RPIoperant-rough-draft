
#!/usr/bin/python3


# third party imports 
import RPi.GPIO as GPIO


class Button(): 
    def __init__(self, button_dict): 

        self.door = button_dict['name']
        self.function = button_dict['function']
        self.name = (f'{self.function}_{self.door}_button')

        self.pin = button_dict['pin']
        self._gpio_setup_pin() 

    def _gpio_setup_pin(self): 
        GPIO.setup(self.pin, GPIO.IN)



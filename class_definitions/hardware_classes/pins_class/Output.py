
#!/usr/bin/python3

# Standard Library Imports 
import time 

# third party imports 
import RPi.GPIO as GPIO
from pigpio import pi


class Output(): 
    def __init__(self, output_dict): 

        self.name = output_dict['name']

        self.pin = output_dict['pin']
        self._gpio_setup_pin() 
        

    def _gpio_setup_pin(self): 
        GPIO.setup(self.pin, GPIO.OUT)
    

    def pulse_sync_line(self, length): 
        print("P U L S E")
        # self.results.event_queue.put([round, f'pulse sync line ({length})', time.time()-self.start_time])
        timestamp = time.time()
        GPIO.output(self.pin, 1)
        time.sleep(length)
        GPIO.output(self.pin, 0)
        return f'pulse sync line ({length})', timestamp, True


    def buzz(self, buzz_type): 
        if self.name != 'speaker': 
            print(f'attempted a call to the buzz function for the {self.name} pin.')
            return 

        print("B U Z Z")
        if buzz_type is 'round_buzz': 
            buzz_len =  self.key_values['round_start_tone_time']
            hz =  self.key_values['round_start_tone_hz']
            name = 'round_start_tone'
            
        elif buzz_type is 'pellet_buzz': 
            buzz_len = self.key_values['pellet_tone_time']
            hz = self.key_values['pellet_tone_hz']
            name =  'pellet_tone'
            
        elif buzz_type is 'door_open_buzz': 
            buzz_len = self.key_values['door_open_tone_time']
            hz = self.key_values['door_open_tone_hz']
            name = 'door_open_tone'

        elif buzz_type is 'door_close_buzz':
            buzz_len = self.key_values['door_close_tone_time'] 
            hz = self.key_values['door_close_tone_hz']
            name = 'door_close_tone'
        
        else: 
            print('the specified buzz_type passed to the buzz funciton does not exist. check for spelling errors?')
            exit()
        
        pi.set_PWM_dutycycle(self.pin, 255/2)
        pi.set_PWM_frequency(self.pin, int(hz))
        time.sleep(buzz_len)
        pi.set_PWM_dutycycle(self.number, 0) # turn off sound 
        return 
        




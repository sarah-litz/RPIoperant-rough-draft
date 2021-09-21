
#!/usr/bin/python3

# Standard Library Imports 
import time 

# third party imports 
import RPi.GPIO as GPIO
import pigpio


class Output(): 
    def __init__(self, output_dict, timestamp_q): 

        self.name = output_dict['name']

        self.timestamp_q = timestamp_q

        self.pin = output_dict['pin']
        self._gpio_setup_pin() 

        self.pi = pigpio.pi()
        

    def _gpio_setup_pin(self): 
        GPIO.setup(self.pin, GPIO.OUT)
    

    def pulse_sync_line(self, length, descriptor=None): 
        # print("P U L S E")
        # self.results.event_queue.put([round, f'pulse sync line ({length})', time.time()-self.start_time])
        timestamp = time.time()
        self.timestamp_q.put_item(time.time(), f'pulse sync line ({length})')
        GPIO.output(self.pin, 1)
        time.sleep(length)
        GPIO.output(self.pin, 0)
        if descriptor is not None: 
            return f'pulse sync line, {descriptor} ({length})', timestamp, True
        return f'pulse sync line ({length})', timestamp, True


    def buzz(self, length, hz, buzz_type): 

        # print(f'B U Z Z ({buzz_type})')
        '''if buzz_type is 'round_buzz': 
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
            exit()'''
        
        self.pi.set_PWM_dutycycle(self.pin, 255/2)
        self.pi.set_PWM_frequency(self.pin, int(hz))
        timestamp = time.time()
        self.timestamp_q.put_item(timestamp, f'{buzz_type} (length: {length})')
        time.sleep(int(length))
        self.pi.set_PWM_dutycycle(self.pin, 0) # turn off sound 
        return f'Buzz, {buzz_type}', timestamp, True
        
    def cleanup(self): 
        pass 




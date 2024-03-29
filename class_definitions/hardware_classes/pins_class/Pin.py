''' ----------------------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Pin.py
                            description: Pin objects are instantiated in pin_setup() in ScriptClass.py. Pin Class is the parent class to Lever and Pellet. 
                            ScriptClass defines a descriptive name for each of the pins, and then the Pin class pairs those names with an actual GPIO pin. 
                            Pin Class executes (almost) all of the direct interaction with the GPIO pins. 
                            
                            functions defined that should only get called by a specific pin: 
                                - pulse_sync_line only gets called with 'gpio_sync' pin 
                                - buzz only gets called with 'speaker_tone' pin
                            
                            functions defined that are called by any pin: detect_event, and all the setup funcitons
-------------------------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# standard lib imports 
import time
from queue import Queue
import os 
if os.system('sudo lsof -i TCP:8888'): #activates the pigpio daemon that runs PWM, unless its already running
    os.system('sudo pigpiod')

# third party imports 
import RPi.GPIO as GPIO
from gpiozero import LED, Button 
from adafruit_servokit import ServoKit
import pigpio

# local imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings

# globals and constants 
kit = ServoKit(channels=16)
GPIO.setmode(GPIO.BCM) # set up BCM GPIO numbering 


class Pin(): # class for a single pin 
    def __init__(self, pin_name, pin_number, gpio_obj=None): 
        
        self.name = pin_name
        self.number = pin_number
        # TODO: should only do this gpio_obj setup ONE TIME!! if this has already happened, skip this step 
        self.gpio_obj = self.gpio_setup() # TODO: get rid of obj version 
        self.pi = pigpio.pi()
        self.stop_threads = False # used in continuous monitoring 
        self.event_count = 0 # incremented each time an event is counted. This should get reset each new round. 
        self.pin_event_queue = Queue()
        self.type = 'Pin'
    
    ''' --------- Private Setup Methods --------------'''
    '''def type_setup(self): 
        if 'door' in self.name:
                type = 'door'
        
        return type''' 
    
    def gpio_setup(self): # setup with GPIO and create new instance based on type where necessary. (accessed thru self.type_instance)
       
        # GPIO setup 
        if 'lever' in self.name or 'switch' in self.name: # QUESTION/TODO: or 'door' in self.name:
            print(f'{self.name}|{self.number}: IN')
            GPIO.setup(self.number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            return GPIO 
        elif 'read' in self.name:
            print(f'{self.name}|{self.number}: IN')
            GPIO.setup(self.number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            return GPIO
        elif 'led' in self.name or 'dispense' in self.name :
            GPIO.setup(self.number, GPIO.OUT)
            GPIO.output(self.number, 0)
            print(f'{self.name}|{self.number}: OUT')
            return GPIO
        else:
            GPIO.setup(self.number, GPIO.OUT)
            print(f'{self.name}|{self.number}: OUT')
            return GPIO
    
 
    ''' ---------- Public Methods --------------- '''        
    # TODO: throw errors if pulse_sync_line or buzz are called with a pin that isn't their defined pin.
    def pulse_sync_line(self, length): # always called for the 'gpio_sync' pin
        GPIO.output(self.number, 1)
        time.sleep(length)
        GPIO.output(self.number, 0)
        return 
    
    def buzz(self, buzz_len, hz): # always called with the 'speaker_tone' pin
        # QUESTION: not using buzz_len?? 
        # call with the speaker tone pin 
        self.pi.set_PWM_dutycycle(self.number, 255/2)
        self.pi.set_PWM_frequency(self.number, int(hz))
        time.sleep(buzz_len)
        self.pi.set_PWM_dutycycle(self.number, 0) # turn off sound 
        return 
    
    
    
    #   Pin Event Detection           
    def detect_event(self, timeout, edge=None): # detects the current pin for the occurence of some event
        ''' waits for event to happen to the current pin. As soon as there is an event detected the function returns'''
        
        # defaults to rising edge, but can change this by passing in arg for edge
        if edge is None: 
            GPIO.add_event_detect(self.number, GPIO.RISING, bouncetime=200) 
        else: 
            GPIO.add_event_detect(self.number, edge, bouncetime=200)
            
        print(f'waiting for an event at: {self.name} ({self.number})')
        start = time.time()
        while True:
            if GPIO.event_detected(self.number):
                timestamp = time.time()
                print(f'event detected for {self.name} at {timestamp}')
                GPIO.remove_event_detect(self.number)
                return True, timestamp
            if time.time() - start > timeout:
                print(f'{self.name} timeout')
                timestamp = time.time()
                GPIO.remove_event_detect(self.number)
                return False, timestamp 
            time.sleep(0.025)

    
    def reset(self): # for resetting values between script runs 
        self.stop_threads = False # used in continuous monitoring 
        self.event_count = 0 # incremented each time an event is counted. This should get reset each new round. 
    
    def cleanup(): 
        pass 
            
    '''
    
    # --------------- NOT IN USE ANYMORE ---------
    def old_detect_event(self, timeout): # TODO: delete this at somepoint if new detect_event is working better    
        try:         
            channel = GPIO.wait_for_edge(self.number, GPIO.RISING, timeout=(timeout*1000)) # timeout based on key_values['Time II']
            if channel is None: 
                print(f"{self.name} timed out. no event detected (Pin.py)")
                return False
            else: 
                print(f'Edge detected for {self.name} in detect_event function (Pins.py)' )
                return True
        
        except KeyboardInterrupt: 
            GPIO.cleanup()
    
    BUTTON PRESS DETECTED: couldn't get to work, replaced with detect_event function
    def button_press_detected_callback(self): 
        print("button was pressed")
    def detect_button_press(self, timeout): 
        button = Button(self.number)
        button.wait_for_press(timeout)
        if(button.is_pressed): 
            button.when_pressed = (self.button_press_detected_callback)
        else: 
            print("no press detected")
            
    def read_gpio_status(self):  # not in use anymore 
        return GPIO.input(self.number)
    '''


            
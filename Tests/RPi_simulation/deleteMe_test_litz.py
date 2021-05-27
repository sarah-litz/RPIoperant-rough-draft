#!/usr/bin/python3
#from gpiozero import Button
#from signal import pause

import pigpio
import Tests.RPi_simulation.GPIO_simulation as GPIO # this was causing me so many issues idk 
import GPIOEmulator as GPIO # mock raspberry pi
import time
import traceback

'''from EmulatorGUI import GPIO # GPIOSimulator-0.1 
from GPIOSimulator import GPIO
python from GPIOEmulator.EmulatorGUI import GPIO'''

pins = {'lever_food':27,
    'lever_door_1':18,
    'lever_door_2':22,
    'led_food':19,
    'read_pellet':16,
    'speaker_tone':21,
    'led_social':20,
    'door_1_override_open_switch':24,
    'door_2_override_open_switch':6,
    'door_1_override_close_switch':25,
    'door_2_override_close_switch':5,
    'door_1_state_switch':4,
    'door_2_state_switch':17,
    'read_ir_1':12,
    'read_ir_2':13,

    'gpio_sync':23, }

    

GPIO.setup(pins[0], GPIO.IN)

def Main():
    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(4, GPIO.OUT) 
        GPIO.setup(17, GPIO.OUT, initial = GPIO.LOW) 
        GPIO.setup(18, GPIO.OUT, initial = GPIO.LOW) 
        GPIO.setup(21, GPIO.OUT, initial = GPIO.LOW) 
        GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
        GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 
        GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 
        GPIO.setup(26, GPIO.IN)

        while(True):
            if (GPIO.input(23) == False):
                GPIO.output(4,GPIO.HIGH) 
                GPIO.output(17,GPIO.HIGH) 
                time.sleep(1)
            if (GPIO.input(15) == True):
                GPIO.output(18,GPIO.HIGH) 
                GPIO.output(21,GPIO.HIGH) 
                time.sleep(1)
            if (GPIO.input(24) == True):
                GPIO.output(18,GPIO.LOW) 
                GPIO.output(21,GPIO.LOW) 
                time.sleep(1)
            if (GPIO.input(26) == True):
                GPIO.output(4,GPIO.LOW) 
                GPIO.output(17,GPIO.LOW) 
                time.sleep(1)
    except Exception as ex:
        traceback.print_exc()
    finally:
        GPIO.cleanup() #this ensures a clean exit

Main()
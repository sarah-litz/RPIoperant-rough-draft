

# standard lib imports
import time
import pigpio 
import RPi.GPIO as GPIO
from gpiozero import LED, Button 
from adafruit_servokit import ServoKit
# Local Imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings




class Servo(): 
    __init__(self): 
        

    def get_door_id(self, door_pin): 
        # if this gets passed "lever_door_1", then the function will just return 'door_1'
            door = door_pin          
            num_filtered = filter(str.isdigit, door) # filter out non-numeric characters 
            num = "".join(num_filtered) # merges numbers into one string 
            return("door_" + num)
    def set_servo(self):         
        all_doors = self.get_pins_of_type('door')
        numlist = []
        print("ALL DOORS OF TYPE DOOR: ", all_doors)
        for d in all_doors: 
            numlist.append(self.get_door_id(d)) 
        print("NUMBER LIST IS: ")
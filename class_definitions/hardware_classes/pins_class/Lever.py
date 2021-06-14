
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: lever.py
                    description: 
                        Includes the following classes: 
                            - Lever(Pin)
                            - Door(Lever)
                            - Food(Lever)
-----------------------------------------------------------------------------------------------------------------------------------'''
# standard lib imports
import time
import pigpio 
import RPi.GPIO as GPIO
from gpiozero import LED, Button 
from adafruit_servokit import ServoKit
# Local Imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.Pin import Pin

# constants 
    
class Lever(Pin): 
    # LEVER TYPE: lever_IDs can be "food", "door_1", or "door_2" 
    # CONTROLLED BY SERVOS ( accessed thru servo_dict in original code )

    def __init__(self, pin_name, pin_number, type=None, gpio_obj=None, lever_angles=None, servo_dict=None, continuous_servo_speed=None): 
        super().__init__(pin_name, pin_number, gpio_obj)
        # inherits from Pin: self.key (pin_name), self.number, self.gpio_obj
        # option to pass in user defined values, otherwise default values from operant_cage_settings_default.py are used
        
        # attributes specific to the Pellet Lever 
        self.lever_angle = self.set_lever_angle(lever_angles)
        # attributes specific to Lever 
        self.servo = self.set_servo_dict_value(servo_dict)
        self.continuous_servo_speed = self.set_continuous_servo_speed(continuous_servo_speed)
        
        self.type = 'Lever'
        
    ''' ------------ Private Methods ------------ '''
    '''methods for looking up and setting the pin_name's corresponding values '''
    # using <pin_name> as key, lookup the corresponding values in servo_dict, continuous_servo_speeds, and lever_angles 
    def set_lever_angle(self, lever_angles):     
        if (lever_angles == None): 
            if 'food' in self.key: 
                return default_operant_settings.lever_angles.get('food')
            elif 'door_1' in self.key: 
                return default_operant_settings.lever_angles.get('door_1')
            elif 'door_2' in self.key: return default_operant_settings.lever_angles.get('door_2')
            else: pass 
        else: return lever_angles
            
    def set_servo_dict_value(self, servo_dict): 
        if (servo_dict == None): 
            return default_operant_settings.servo_dict.get(self.key)            
        else: return servo_dict
        
    def set_continuous_servo_speed(self, continuous_servo_speed):
        if (continuous_servo_speed == None):
            if 'food' in self.key: 
                return default_operant_settings.continuous_servo_speeds.get('dispense_pellet')
            elif ('door_1' in self.key): 
                return default_operant_settings.continuous_servo_speeds.get('door_1') 
            elif 'door_2' in self.key: return default_operant_settings.continuous_servo_speeds.get('door_2')
            else: pass 
        else: return continuous_servo_speed
    
    ''' ------------ Public Methods ---------------- '''





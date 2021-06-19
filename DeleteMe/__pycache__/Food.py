

from class_definitions.hardware_classes.pins_class.Pin import Pin
from class_definitions.hardware_classes.pins_class.Lever import Lever
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
import time

TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 


class Food(): 
    def __init__(self, this_foods_pins, food_id=None): # if more food pins ever added, option to pass in a food_id to specificy which Food instance 
        
        # set food_id if applicable 
        if food_id is None: 
            self.food_id = 'food'
        else: self.food_id = food_id
        
        # Pin Setup
        self.lever = this_foods_pins[f'lever_{self.food_id}']
        self.led = this_foods_pins[f'led_{self.food_id}']
        self.read_pellet = this_foods_pins['read_pellet']
        
        # Servo Setup 
        # -->self.servo_lever = default_operant_settings.servo_dict.get(f'lever_{self.food_id}')
        self.servo_dispense_pellet = default_operant_settings.servo_dict.get(f'dispense_pellet')
        
        # Servo Values Setup 
        # -->self.lever_angles = default_operant_settings.lever_angles.get(f'{self.food_id}')
        self.continuous_servo_speeds = default_operant_settings.continuous_servo_speeds.get('dispense_pellet')
        
        # Setup the Lever Pin's angle values: 
        # -->self.lever.angle = self.lever_angles
        
        self.type='Food'
    
    
    ''' Lever Methods '''
    # Lever Functions 
    '''def extend_lever(self): 
        self.lever.extend_lever()
    def retract_lever(self): 
        self.lever.retract_lever()'''
        
    # Pin Functions
    def detect_event(self, timeout): 
        self.lever.detect_event(timeout)  # gets pin object and calls the detect_event function for that pin
        
        
        

        '''print("(EXTENDING LEVER) lever angle: ", self.lever_angles)
        extend = self.lever_angles[0]
        retract = self.lever_angles[1]
        
        #we will wiggle the lever a bit to try and reduce binding and buzzing
        modifier = 15
        if extend > retract:
            extend_start = extend + modifier
        else:
            extend_start = extend - modifier
        
        self.servo_lever.angle = extend_start 
        time.sleep(0.1)
        self.servo_lever.angle = extend''' 
    

        '''print("(RETRACTING LEVER) lever angle: ", self.lever_angles)
        retract = self.lever_angles[1]   
        
        start = time.time() 
        self.servo_lever.angle = retract''' 
    
    
        
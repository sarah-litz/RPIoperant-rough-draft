

from class_definitions.hardware_classes.pins_class.Lever import Lever
import time

TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 


class Food(Lever): 
    def __init__(self, pin_name, pin_number, type=None, gpio_obj=None, lever_angles=None, servo_dict=None, continuous_servo_speed=None): 
        super().__init__(pin_name, pin_number, gpio_obj, lever_angles, servo_dict, continuous_servo_speed)
        self.type = 'Food'
        
    def extend_lever(self): 
        print("(EXTENDING LEVER) lever angle: ", self.lever_angle)
        extend = self.lever_angle[0]
        retract = self.lever_angle[1]
        
        #we will wiggle the lever a bit to try and reduce binding and buzzing
        modifier = 15
        if extend > retract:
            extend_start = extend + modifier
        else:
            extend_start = extend - modifier
        
        self.servo.angle = extend_start 
        time.sleep(0.1)
        self.servo.angle = extend 
    
    def retract_lever(self): 
        print("(RETRACTING LEVER) lever angle: ", self.lever_angle)
        retract = self.lever_angle[1]   
        
        start = time.time() 
        self.servo.angle = retract 
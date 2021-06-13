
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

# Local Imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.Pins import Pin

# constants 
TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 
    
class Lever(Pin): 
    # LEVER TYPE: lever_IDs can be "food", "door_1", or "door_2" 
    # CONTROLLED BY SERVOS ( accessed thru servo_dict in original code )

    def __init__(self, pin_name, pin_number, type=None, gpio_obj=None, lever_angles=None, servo_dict=None, continuous_servo_speed=None): 
        super().__init__(pin_name, pin_number, gpio_obj)
        # inherits from Pin: self.key (pin_name), self.number, self.gpio_obj
        # option to pass in user defined values, otherwise default values from operant_cage_settings_default.py are used
        
        # attributes specific to Lever
        self.lever_angle = self.set_lever_angle(lever_angles)
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
            else: return default_operant_settings.lever_angles.get('door_2')
            # else: return lever_angles
            
    def set_servo_dict_value(self, servo_dict): 
        if (servo_dict == None): 
            return default_operant_settings.servo_dict.get(self.key)
        else: return servo_dict.get(self.pin_name)
        
    def set_continuous_servo_speed(self, continuous_servo_speed):
        if (continuous_servo_speed == None):
            print(default_operant_settings.continuous_servo_speeds.get(self.key))
            return default_operant_settings.continuous_servo_speeds.get(self.key)
        else: return continuous_servo_speed
    
    ''' ------------ Public Methods ---------------- '''



class Door(Lever): 
    def __init__(self, pin_name, pin_number, type=None, gpio_obj=None, lever_angles=None, servo_dict=None, continuous_servo_speed=None): 
        super().__init__(pin_name, pin_number, type, gpio_obj, lever_angles, servo_dict, continuous_servo_speed)
        
        # attributes specific to Door 
        self.type = 'Door'
        self.door_state = False # initialize door state to False
        
    ''' DOOR METHODS '''
    def isOpen(self): 
        if not self.gpio_obj.input(self.number):
            print(f'{self.key} is open')
            self.door_state = True
            return self.door_state
        else: 
            self.door_state = False
            return self.door_state
        
    def open_door(self):
        ''' opens the door of the Lever object that calls this method '''
        ''' if we want to open a list of doors, will need to call this method for each object in the list '''
        
        # QUESTION/TODO: self.pin_name does not always line up with the name we need to use to access the operant_cage_settings_default dictionaries. Why is this?? 
        # door_id = self.pin_name
        if self.isOpen(): 
            # door is already open 
            return
        
        self.servo.throttle =  self.continuous_servo_speed['open']
        open_time = self.continuous_servo_speed['open time']
        start = time.time()

        while time.time() < ( start + open_time ): # and not self.door_override[door_id]:
            #wait for the door to open
            time.sleep(0.05)

        #door should be open!
        self.servo.throttle = self.continuous_servo_speed['stop']

        print('exiting door open attempts')

            
        '''if not gpio_obj.input(pins[f'{door_ID}_state_switch']):
            if self.door_override[door_ID]:
                print(f'open {door_ID} stopped due to override!')
            print(f'{door_ID} failed to open!!!')
            self.timestamp_queue.put('%i, %s open failure, %f'%(self.round, door_ID, time.time()-self.start_time))
        else:
            self.timestamp_queue.put('%i, %s open finish, %f'%(self.round, door_ID, time.time()-self.start_time))
            self.door_states[door_ID] = False'''
    
    def close_door(self): # close the current door
        # QUESTION/TODO: compare this version to the original version of close_door, I changed kinda a lot and want to ensure those changes will work
        #check if the doors are open
        if not self.isOpen(): 
            # door is already closed 
            return 
        
        start = time.time()

        self.servo.throttle = self.continuous_servo_speed['close']
        while self.isOpen() and time.time()-start < TIMEOUT: pass 
        if not self.isOpen(): # check if door successfully shut
            self.door_state = True
            self.servo.throttle = self.continuous_servo_speed['stop']
            print("close door function was here")
        else: 
            print(f'ah crap, door {self.number} didnt close!') 
                #if not self.door_override[door_ID]:
                # self.servo.throttle = self.continuous_servo_speed['close'] # QUESTION/TODO: why do we have to continuously set this ?? can this go outside of the while loop? 
                #we will close the door until pins for door close are raised, or until timeout
                # if not GPIO.input(pins[f'{door_ID}_state_switch']): # QUESTION/TODO: what is this line checking for??                 

class Food(Lever): 
    def __init__(self, pin_name, pin_number, type=None, gpio_obj=None, lever_angles=None, servo_dict=None, continuous_servo_speed=None): 
        super().__init__(pin_name, pin_number, type, gpio_obj, lever_angles, servo_dict, continuous_servo_speed)
    
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
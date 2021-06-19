
# standard lib imports
import time 

# third party imports 
import RPi.GPIO as GPIO

# local imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.Lever import Lever


TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 

class Door(Lever): 
    def __init__(self, pin_name, pin_number, type=None, gpio_obj=None, lever_angles=None, servo_dict=None, continuous_servo_speed=None): 
        super().__init__(pin_name, pin_number, gpio_obj, lever_angles, servo_dict, continuous_servo_speed)
        
        # change the servo attribute set in Lever 
        # self.servo = self.set_doors_servo_dict_values()
        
        # attributes specific to Door 
        self.type = 'Door'
        self.door_state = False # initialize door state to False
        
    ''' DOOR METHODS '''
    def isOpen(self): 
        if self.gpio_obj.input(self.number):
            # print(f'{self.key} is open')
            self.door_state = True
            return self.door_state
        else: 
            self.door_state = False
            return self.door_state
    

    def get_door_id(self): 
        # if this gets passed "lever_door_1", then the function will just return 'door_1' 
        if 'door' in self.key: 
            num_filtered = filter(str.isdigit, self.key) # filter out non-numeric characters 
            num = "".join(num_filtered) # merges numbers into one string 
            return("door_" + num)
    
    def set_doors_servo_dict_values(self): 
        door_id = self.get_door_id()
         
        self.servo = [default_operant_settings.servo_dict.get(self.key)]
        self.servo.append(default_operant_settings.servo_dict.get(door_id) )
        
    def open_door(self):
        ''' opens the door of the Lever object that calls this method '''
        ''' if we want to open a list of doors, will need to call this method for each object in the list '''
        
        # QUESTION/TODO: self.pin_name does not always line up with the name we need to use to access the operant_cage_settings_default dictionaries. Why is this?? 
        # door_id = self.pin_name
        if self.isOpen(): 
            # door is already open 
            print(f'{self.key} was already open')
            return
        
        self.servo.throttle =  self.continuous_servo_speed['open']
        open_time = self.continuous_servo_speed['open time']
        start = time.time()

        while time.time() < ( start + open_time ): # and not self.door_override[door_id]:
            #wait for the door to open
            time.sleep(0.05)

        #door should be open!
        self.servo.throttle = self.continuous_servo_speed['stop']
        self.door_state = True # True = Open Door, False = Closed Door 

        print('exiting door open attempts')

            
        '''if not gpio_obj.input(pins[f'{door_ID}_state_switch']):
            if self.door_override[door_ID]:
                print(f'open {door_ID} stopped due to override!')
            print(f'{door_ID} failed to open!!!')
            self.timestamp_queue.put('%i, %s open failure, %f'%(self.round, door_ID, time.time()-self.start_time))
        else:
            self.timestamp_queue.put('%i, %s open finish, %f'%(self.round, door_ID, time.time()-self.start_time))
            self.door_states[door_ID] = False'''
    
    def close_door(self, state_switch_pin): # close the current door. Need the state_switch pin as well, so passing in instance of that also 
        # QUESTION/TODO: compare this version to the original version of close_door, I changed kinda a lot and want to ensure those changes will work
        self.door_state = True 
        #check if doors are already closed
        if self.door_state is False: # False for closed door, True for open door 
            print(f'{self.key} is already closed')
            return 
        
        start = time.time()

        # QUESTION/TODO: if I want to close door_1, do I call it on the servo "lever_door_1" or "door_1" ??? 
        print("closing speed:", self.continuous_servo_speed['close'])
        
        ''' TESTING different servo values ''' 
        
        print("SERVO VALUE IS: ",  self.servo, " and the servo speed is: ", self.continuous_servo_speed['close'])
        self.servo.throttle = self.continuous_servo_speed['close']
        
        
        while self.door_state is True and time.time()-start < TIMEOUT:  
            # repeatedly check the state switch pin to see if the door has shut
            if not GPIO.input(state_switch_pin.number): 
                # door shut successfully, stop the door 
                self.door_state = False # ?? which pins door_state should I update? 'lever_door_1' or 'door_1'
                self.servo.throttle = self.continuous_servo_speed['stop']
            else: 
                pass # if it does not shut, pass until we reach the TIMEOUT limit 

        # check the reason for exiting the while loop: (either door closed, or reached timeout)
        if self.door_state is False: 
            # door is closed 
            print(f'{self.key} should be closed now! ')
            # TODO: check the state switch 
            # TODO: override door
        else: 
            print(f'ah crap, door {self.key} didnt close!') 
                
        
                #if not self.door_override[door_ID]:
                # self.servo.throttle = self.continuous_servo_speed['close'] # QUESTION/TODO: why do we have to continuously set this ?? can this go outside of the while loop? 
                #we will close the door until pins for door close are raised, or until timeout
                # if not GPIO.input(pins[f'{door_ID}_state_switch']): # QUESTION/TODO: what is this line checking for??                 




# standard lib imports
import time 

# third party imports 
import RPi.GPIO as GPIO

# local imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings


TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 

class Door(): 
    def __init__(self, door_id, this_doors_pins): # dictionary of pin objects is passed in 
        
        print("This_Doors_Pins: ", this_doors_pins.items())
        for p in this_doors_pins.values(): 
            print("DOOR TYPE bb : ", p.name)
        
        self.door_id = door_id # doesn't matter which pin we check cause all should have same door_id
    
        
        # Servo Setup 
        # self.servo_lever = default_operant_settings.servo_dict.get(f'lever_{door_id}')
        self.servo_door = default_operant_settings.servo_dict.get(f'{door_id}')
        
        # Servo Values Setup
        self.lever_angles = default_operant_settings.lever_angles.get(f'{door_id}')
        self.continuous_servo_speed  = default_operant_settings.continuous_servo_speeds.get(f'{door_id}')
        
        
        # Pin Setup
        self.override_open_switch = this_doors_pins[f'{door_id}_override_open_switch']
        self.override_close_switch = this_doors_pins[f'{door_id}_override_close_switch']
        self.state_switch = this_doors_pins[f'{door_id}_state_switch']
        self.lever = this_doors_pins[f'lever_{door_id}']
        
        
        # Tracking Door States 
        self.open = False # state of door; if True, the door is open. if False, door is closed. 
        self.door_override = False # if user needs to manually override door funcitonality w/ buttons, this becomes True
        
    ''' DOOR METHODS '''

    
    def get_door_id(self, name): 
        # if this gets passed "lever_door_1", then the function will just return 'door_1' 
        if 'door' in name: 
            num_filtered = filter(str.isdigit, name) # filter out non-numeric characters 
            num = "".join(num_filtered) # merges numbers into one string 
            return("door_" + num)
    
    '''def set_doors_servo_dict_values(self): 
        door_id = self.get_door_id()
         
        self.servo = [default_operant_settings.servo_dict.get(self.key)]
        self.servo.append(default_operant_settings.servo_dict.get(door_id) )'''
        
    def open_door(self):
        ''' opens the door of the Lever object that calls this method '''
        ''' if we want to open a list of doors, will need to call this method for each object in the list '''
        
        if self.open is True: 
            # door is already open 
            print(f'{self.door_id} was already open')
            return
        
        self.servo_door.throttle =  self.continuous_servo_speed['open']
        open_time = self.continuous_servo_speed['open time']
        start = time.time()

        while time.time() < ( start + open_time ): # and not self.door_override[door_id]:
            #wait for the door to open
            time.sleep(0.05)

        #door should be open when we hit this point 
        self.servo_door.throttle = self.continuous_servo_speed['stop']
        
        # Check that door successfully opened
        if self.state_switch: 
            self.open = True # True = Open Door, False = Closed Door 
            print(f'{self.door_id} should be open now!')
            
        else: # Check for Door Override 
            if not self.door_override: 
                print(f'open {self.door_id} stopped due to override!')
            print(f'{self.door_id} failed to open')
            self.open = False 
            
    
    def close_door(self): # close the current door. Need the state_switch pin as well, so passing in instance of that also 
        # QUESTION/TODO: compare this version to the original version of close_door, I changed kinda a lot and want to ensure those changes will work
        self.open = True 
        #check if doors are already closed
        if self.open is False: # False for closed door, True for open door 
            print(f'{self.name} is already closed')
            return 
        
        start = time.time()

        # QUESTION/TODO: if I want to close door_1, do I call it on the servo "lever_door_1" or "door_1" ??? 
        print("closing speed:", self.continuous_servo_speed['close'])
        self.servo_door.throttle = self.continuous_servo_speed['close']
        
        while self.open is True and time.time()-start < TIMEOUT:  
            # repeatedly check the state switch pin to see if the door has shut
            if not GPIO.input(self.state_switch.number): 
                # door shut successfully, stop the door 
                self.open = False # ?? which pins door_state should I update? 'lever_door_1' or 'door_1'
                self.servo_door.throttle = self.continuous_servo_speed['stop']
            else: 
                pass # if it does not shut, pass until we reach the TIMEOUT limit 

        # check the reason for exiting the while loop: (either door closed, or reached timeout)
        if self.open is False: 
            # door is closed 
            print(f'{self.door_id} should be closed now! ')
            # TODO: check the state switch 
            # TODO: override door
        else: 
            print(f'ah crap, door {self.door_id} didnt close!') 
                
        
                #if not self.door_override[door_ID]:
                # self.servo.throttle = self.continuous_servo_speed['close'] # QUESTION/TODO: why do we have to continuously set this ?? can this go outside of the while loop? 
                #we will close the door until pins for door close are raised, or until timeout
                # if not GPIO.input(pins[f'{door_ID}_state_switch']): # QUESTION/TODO: what is this line checking for??                 

    
    def override_door(self): 
        
        while True: 
            if not GPIO.input(self.override_open_switch): 
                self.door_override = True 
                self.servo_door.throttle = self.continuous_servo_speed['open']
                while not GPIO.input(self.override_open_switch): 
                    time.sleep(0.05)
                self.servo_door.throttle = self.continuous_servo_speed['stop']
            
            if not GPIO.input(self.override_close_switch): 
                self.door_override = True 
                self.servo_door.throttle = self.continuous_servo_speed['close']
                while not GPIO.input(self.override_close_switch): 
                    time.sleep(0.05)
                self.servo_door.throttle = self.continuous_servo_speed['stop']
            
            self.door_override = False
            
            time.sleep(0.1)

    
        

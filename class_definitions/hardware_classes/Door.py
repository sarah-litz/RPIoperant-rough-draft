''' ----------------------------------------------------------------------------------------------------------------------------------------------
                                                            filename: Door.py
                            description: Door objects are instantiated in ScriptClass.py in door_setup. This happens after pin_setup is complete
                            because Door class needs to access/build upon multiple pins, so we must wait till those have already been set. 
                            Door.py gives access to functions that only apply to Doors including opening/closing doors and having threads that are 
                            dedicated to monitoring the override buttons (green/red buttons).  which if pressed will manually control the doors. 
                            
                            Note on the Override Buttons: 
                                Green Button (pin: override_open_switch) -- Press to OPEN door 
                                Red Button (pin: override_close_swtich) -- Press to CLOSE door 
-------------------------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# standard lib imports
import time 
import threading 

# third party imports 
import RPi.GPIO as GPIO

# local imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings

# globals 
TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 

        
class Door(): 
    def __init__(self, door_dict): # , door_id, this_doors_pins): # dictionary of pin objects is passed in 
        
        
        print(f">> New Door Created: {door_dict['name']} << ")
        
        # name vs door_id????? 
        # self.door_id = door_dict['name'] # all pins in this_doors_pins will have the same door_id (e.g. 'door_1')
        self.name = door_dict['name']

        #
        # Servo Stuff 
        #   
        self.servo = door_dict['servo']
        self.stop_speed = door_dict['stop']
        self.open_speed = door_dict['open']
        self.close_speed = door_dict['close']

        # 
        # Button Stuff
        #
        self.buttons = {} # box class adds to this dict 
    
    
        # Servo Setup 
    ''' self.servo_door = default_operant_settings.servo_dict.get(f'{door_id}')
        
        # Servo Values Setup
        self.lever_angles = default_operant_settings.lever_angles.get(f'{door_id}')
        self.continuous_servo_speed  = default_operant_settings.continuous_servo_speeds.get(f'{door_id}')
        
        # Pin Setup: pins for the buttons that override the door that is opening/closing at the time 
        self.override_open_switch = this_doors_pins[f'{door_id}_override_open_switch']
        self.override_close_switch = this_doors_pins[f'{door_id}_override_close_switch'] 
        print(f'{self.door_id} override pin numbers are: (1) Open Switch: {self.override_open_switch.number} (2) Close Switch: {self.override_close_switch.number}')       
        # Pin Setup: pins for the doors 
        self.state_switch = this_doors_pins[f'{door_id}_state_switch'] # this pin will switch when the door successfully closes/open
        self.lever = this_doors_pins[f'lever_{door_id}'] # lever for controlling the door itself?? 
        
        # Tracking Door States 
        # self.open = GPIO.input(self.state_switch.number) # state of door; if True, the door is open. if False, door is closed. 
        self.open_override = False # if user needs to manually override door funcitonality w/ buttons, this becomes True
        self.close_override = False
        
        # Threads for running in the background to monitor the override buttons 
        self.stop_threads = False 
        self.t1 = threading.Thread(target=self.monitor_override_button, args=('green',), daemon=True)
        self.t1.start() # Manually open door with this button 
        self.t2 = threading.Thread(target=self.monitor_override_button, args=('red',), daemon=True)
        self.t2.start() '''
        
        
    ''' DOOR METHODS '''

    def get_door_id(self, name): 
        # if this gets passed "lever_door_1", then the function will just return 'door_1' 
        if 'door' in name: 
            num_filtered = filter(str.isdigit, name) # filter out non-numeric characters 
            num = "".join(num_filtered) # merges numbers into one string 
            return("door_" + num)
    
    def isOpen(self, state_button): # check if door is open 
        
        if state_button: 
            False # door closed 
        else: 
            True # door open 
        
        # return GPIO.input(self.state_switch.number) # returns True if door is open, False if it is not open aka is closed 
    
        
    def open_door(self):
        ''' opens the door of the Lever object that calls this method '''
        ''' if we want to open a list of doors, will need to call this method for each object in the list '''
        if self.isOpen(): 
            # door is already open 
            print(f'{self.name} was already open')
            return
        
        if self.close_override is True: # override button was pressed, exit. 
            print(f'open {self.name} stopped due to override!')
            return 
        
        self.servo.throttle =  self.open_speed
        start = time.time()

        while time.time() < ( start + self.open_time ): # and not self.door_override[door_id]:
            #wait for the door to open -- we just have to assume this will take the exact same time of <open_time> each time, since we don't have a switch to monitor for if it opens all the way or not. 
            if self.close_override is True: # check if override button has been pressed during this time 
                print(f'open {self.name} stopped due to override!')
                return 
            # else: 
            #     time.sleep(0.05)

        #door should be open when we hit this point 
        self.servo.throttle = self.stop_speed
        
        # Check that door successfully opened
        # if self.state_switch: 
        if self.isOpen(): 
            # self.open = True # True = Open Door, False = Closed Door 
            print(f'{self.name} should be open now!')
            
        else: # timed out while trying to open the door 
            print(f'{self.name} failed to open')
            # self.open = False 
            
    
    def close_door(self, state_button): 

        #check if doors are already closed
        if not state_button: # False for closed door, True for open door 
            print(f'{self.name} is already closed')
            return 
        
        # TODO: check for door override button press 
        
        start = time.time()
        self.servo.throttle = self.close_speed
        print('isOpen: ', self.isOpen())
        print('time: ', time.time()-start)
        while state_button and time.time()-start < TIMEOUT:  
            pass 
            # repeatedly check the state switch pin to see if the door has shut
            # check each iteration to make sure door has not been overriden by button

            #if not GPIO.input(self.state_switch.number): 
                # door shut successfully, stop the door 
                # self.open = False 
            #    self.servo_door.throttle = self.continuous_servo_speed['stop'] # might not need this line here.
                
        self.servo.throttle = self.stop_speed
        # check the reason for exiting the while loop: (either door actually closed, or reached timeout)
        if not state_button: # door successfully closed 
            print(f'{self.name} should be closed now! ')
        else: 
            print(f'ah crap, door {self.name} didnt close!') 
        return   
        
                #if not self.door_override[door_ID]:
                # self.servo.throttle = self.continuous_servo_speed['close'] # QUESTION/TODO: why do we have to continuously set this ?? can this go outside of the while loop? 
                #we will close the door until pins for door close are raised, or until timeout
                # if not GPIO.input(pins[f'{door_ID}_state_switch']): # QUESTION/TODO: what is this line checking for??                 

    
    def monitor_override_button(self, color): 
        
        if color is 'green': # button to open door 
            GPIO.add_event_detect(self.override_open_switch.number, GPIO.FALLING, bouncetime=200)  # wait for button to be pressed 
            while True: 
                if GPIO.event_detected(self.override_open_switch.number): # event was detected  
                    self.open_override = True 
                    print('The Green Button was Pressed. Opening the door now...')
                    self.servo_door.throttle = self.continuous_servo_speed['stop'] # immediately stop door motion for quickest response. Then call open door function 
                    self.open_door()
                    self.open_override = False 
                if self.stop_threads is True: 
                    break 

                    
        elif color is 'red': # button to close door (to override an open/opening door)
            GPIO.add_event_detect(self.override_close_switch.number, GPIO.FALLING, bouncetime=200) 
            while True: 
                if GPIO.event_detected(self.override_close_switch.number): 
                    self.close_override = True 
                    print('The Red Button was Pressed. Closing the door now...')
                    self.servo_door.throttle = self.continuous_servo_speed['stop'] # immediately stop door, then call close door 
                    self.close_door()
                    self.close_override = False 
                if self.stop_threads is True: 
                    break  
        
        else: 
            # stop moving the door and throw error 
            print('didnt recognize the argument passed to monitor override button so stopping this door just in case') 
            self.servo_door.throttle = self.continuous_servo_speed['stop']
            return 
        
        # TODO: remove event detection?? Not sure where to place this though. (Maybe in a cleanup function??)
        # note that threads running this function are daemon threads, so will automatically be killed when the main thread is killed. 

            
    def cleanup(self): 
        # QUESTION: should we ensure doors are open and/or closed when we finish?? 
        # kill threads 
        if self.isOpen(): 
            self.close_door() 
        self.stop_threads = True 
        GPIO.remove_event_detect(self.override_open_switch.number)
        GPIO.remove_event_detect(self.override_close_switch.number)

        # emergency stop: 
        self.servo_door.throttle = self.continuous_servo_speed['stop']  # force shutoff if any servos are left moving
        
        self.t1.join()
        self.t2.join()
        
    
             
        
        
    '''def override_door(self): 
        print("IN THE FUNCITON  override_door")
        while True: 
            
            if not GPIO.input(self.override_open_switch.number): # Force Open Door
                self.door_override = True 
                self.servo_door.throttle = self.continuous_servo_speed['open']
                while not GPIO.input(self.override_open_switch.number): # check to see if door has fully opened ( i think?? QUESTION -- wut is this line )
                    time.sleep(0.05)
                self.servo_door.throttle = self.continuous_servo_speed['stop']
            
            if not GPIO.input(self.override_close_switch.number): # Force Close Door
                self.door_override = True 
                self.servo_door.throttle = self.continuous_servo_speed['close']
                while not GPIO.input(self.override_close_switch.number): 
                    time.sleep(0.05)
                self.servo_door.throttle = self.continuous_servo_speed['stop']
            
            self.door_override = False
            
            time.sleep(0.1)'''

    
        

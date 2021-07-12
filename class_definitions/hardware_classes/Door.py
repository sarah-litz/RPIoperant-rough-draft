''' ----------------------------------------------------------------------------------------------------------------------------------------------
                                                            filename: Door.py
                            description: Door objects are instantiated in ScriptClass.py in door_setup. This happens after pin_setup is complete
                            because Door class needs to access/build upon multiple pins, so we must wait till those have already been set. 
                            Door.py gives access to functions that only apply to Doors including opening/closing doors and having threads that are 
                            dedicated to monitoring the override buttons (green/red buttons).  which if pressed will manually control the doors. 
                            
                            Note on the Override Buttons: 
                                Green Button (pin: override_close_switch) -- Press to OPEN door 
                                Red Button (pin: override_open_swtich) -- Press to CLOSE door 
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
    def __init__(self, door_id, this_doors_pins): # dictionary of pin objects is passed in 
        
        print(f">> New Door Created: {door_id} << ")
        '''for p in this_doors_pins.values(): 
            print(p.name)'''
        
        self.door_id = door_id # all pins in this_doors_pins will have the same door_id (e.g. 'door_1')
    
        # Servo Setup 
        self.servo_door = default_operant_settings.servo_dict.get(f'{door_id}')
        
        # Servo Values Setup
        self.lever_angles = default_operant_settings.lever_angles.get(f'{door_id}')
        self.continuous_servo_speed  = default_operant_settings.continuous_servo_speeds.get(f'{door_id}')
        
        # Pin Setup: pins for the buttons that override the door that is opening/closing at the time 
        self.override_open_switch = this_doors_pins[f'{door_id}_override_open_switch']
        self.override_close_switch = this_doors_pins[f'{door_id}_override_close_switch']        
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
        self.t2.start()
        
        
    ''' DOOR METHODS '''

    def get_door_id(self, name): 
        # if this gets passed "lever_door_1", then the function will just return 'door_1' 
        if 'door' in name: 
            num_filtered = filter(str.isdigit, name) # filter out non-numeric characters 
            num = "".join(num_filtered) # merges numbers into one string 
            return("door_" + num)
    
    def isOpen(self): # check if door is open 
        return GPIO.input(self.state_switch.number) # returns True if door is open, False if it is not open aka is closed 
    
    '''def set_doors_servo_dict_values(self): 
        door_id = self.get_door_id()
         
        self.servo = [default_operant_settings.servo_dict.get(self.key)]
        self.servo.append(default_operant_settings.servo_dict.get(door_id) )'''
    
    
    def open_door(self):
        ''' opens the door of the Lever object that calls this method '''
        ''' if we want to open a list of doors, will need to call this method for each object in the list '''
        if self.isOpen(): 
            # door is already open 
            print(f'{self.door_id} was already open')
            return
        
        if self.open_override is True: # override button was pressed, exit. 
            print(f'open {self.door_id} stopped due to override!')
            return 
        
        self.servo_door.throttle =  self.continuous_servo_speed['open']
        open_time = self.continuous_servo_speed['open time']
        start = time.time()

        while time.time() < ( start + open_time ): # and not self.door_override[door_id]:
            #wait for the door to open -- we just have to assume this will take the exact same time of <open_time> each time, since we don't have a switch to monitor for if it opens all the way or not. 
            if self.open_override is True: # check if override button has been pressed during this time 
                print(f'open {self.door_id} stopped due to override!')
                return 
            # else: 
            #     time.sleep(0.05)

        #door should be open when we hit this point 
        self.servo_door.throttle = self.continuous_servo_speed['stop']
        
        # Check that door successfully opened
        # if self.state_switch: 
        if self.isOpen(): 
            # self.open = True # True = Open Door, False = Closed Door 
            print(f'{self.door_id} should be open now!')
            
        else: # timed out while trying to open the door 
            print(f'{self.door_id} failed to open')
            # self.open = False 
            
    
    def close_door(self): 

        #check if doors are already closed
        if not self.isOpen(): # False for closed door, True for open door 
            print(f'{self.door_id} is already closed')
            return 
        if not GPIO.input(self.state_switch.number): 
            print('self.open had the wrong value!! fix this')
            print(f'{self.door_id} is already closed')
            # self.open = False
            return 
        
        if self.close_override is True: # check for door override 
                print(f'close {self.door_id} stopped due to override!')
                return 
        
        start = time.time()
        self.servo_door.throttle = self.continuous_servo_speed['close']
        print('isOpen: ', self.isOpen())
        print('time: ', time.time()-start)
        while self.isOpen() and time.time()-start < TIMEOUT:  
            # repeatedly check the state switch pin to see if the door has shut
            if self.close_override is True: # checks each iteration to make sure door has not been overriden by button
                print(f'close {self.door_id} stopped due to override!')
                return 
            #if not GPIO.input(self.state_switch.number): 
                # door shut successfully, stop the door 
                # self.open = False 
            #    self.servo_door.throttle = self.continuous_servo_speed['stop'] # might not need this line here.
                
        self.servo_door.throttle = self.continuous_servo_speed['stop']
        # check the reason for exiting the while loop: (either door actually closed, or reached timeout)
        if not self.isOpen(): # door successfully closed 
            print(f'{self.door_id} should be closed now! ')
        else: 
            print(f'ah crap, door {self.door_id} didnt close!') 
        return   
        
                #if not self.door_override[door_ID]:
                # self.servo.throttle = self.continuous_servo_speed['close'] # QUESTION/TODO: why do we have to continuously set this ?? can this go outside of the while loop? 
                #we will close the door until pins for door close are raised, or until timeout
                # if not GPIO.input(pins[f'{door_ID}_state_switch']): # QUESTION/TODO: what is this line checking for??                 

    
    def monitor_override_button(self, color): 
        
        if color is 'green': # button to open door 
            GPIO.add_event_detect(self.override_close_switch.number, GPIO.FALLING, bouncetime=200)  # wait for button to be pressed 
            while True: 
                if GPIO.event_detected(self.override_close_switch.number): # event was detected  
                    self.close_override = True 
                    print('The Green Button was Pressed. Opening the door now...')
                    self.servo_door.throttle = self.continuous_servo_speed['stop'] # immediately stop door motion for quickest response. Then call open door function 
                    self.open_door()
                    self.close_override = False 
                if self.stop_threads is True: 
                    break 

                    
        elif color is 'red': # button to close door (to override an open/opening door)
            GPIO.add_event_detect(self.override_open_switch.number, GPIO.FALLING, bouncetime=200) 
            while True: 
                if GPIO.event_detected(self.override_open_switch.number): 
                    self.open_override = True 
                    print('The Red Button was Pressed. Closing the door now...')
                    self.servo_door.throttle = self.continuous_servo_speed['stop'] # immediately stop door, then call close door 
                    self.close_door()
                    self.open_override = False 
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
        ''' if self.isOpen(): 
            self.close_door() '''
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

    
        

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
from class_definitions.hardware_classes.pins_class.Button import Button 
# globals 
TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 

        
class Door(): 
 
    def __init__(self, door_dict, door_buttons, timestamp_q, reward = None): # dictionary of pin objects is passed in 
        
        self.timestamp_q = timestamp_q

        self.name = door_dict['name']
        self.type = 'Door'
        self.servo = door_dict['servo']
        self.stop_speed = door_dict['stop']
        self.close_speed = door_dict['close']
        self.open_speed = door_dict['open']
        self.open_time = door_dict['open_time']
        
        self.open_override = door_buttons['open']
        self.close_override = door_buttons['close']
        self.state = door_buttons['state']
    
        # Startup threads for the override buttons 
        # manually open a door with 'open_override' and close with 'close_override'
        self.stop_threads = False  
        self.t1 = threading.Thread( target = self.open_override.monitor_for_button_press, daemon=True )
        self.t2 = threading.Thread( target = self.close_override.monitor_for_button_press, daemon=True )
        self.check_threads = threading.Thread( target = self.monitor_override_buttons, daemon=True )
        self.t1.start() 
        self.t2.start()
        self.check_threads.start() 
    
        # Servo Setup 

        
    ''' # Tracking Door States 
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
    
    def isOpen(self): # check if door is open 
        
        if self.state: 
            return False # door closed 
        else: 
            return True # door open 

    
        
    def open_door(self):
        ''' opens the door of the Lever object that calls this method '''
        ''' if we want to open a list of doors, will need to call this method for each object in the list '''
        if self.state is True: 
            # door is already open 
            print(f'{self.name} was already open')
            return
        
        if self.close_override.flag is True: # override button was pressed, exit. 
            self.servo.throttle = self.stop_speed
            print(f'open {self.name} stopped due to override! Closing door now.')
            self.close_door() 
            return 
        
        start = time.time()
        self.servo.throttle =  self.open_speed

        while time.time() < ( start + self.open_time ): # and not self.door_override[door_id]:
            #wait for the door to open -- we just have to assume this will take the exact same time of <open_time> each time, since we don't have a switch to monitor for if it opens all the way or not. 
            if self.close_override.flag is True: # check if override button has been pressed during this time 
                self.servo.throttle = self.stop_speed
                print(f'open {self.name} stopped due to override! Closing door now.')
                self.close_door() 
                return 
            else: 
                time.sleep(0.005)

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
            

            
    
    def close_door(self): 

        #check if doors are already closed
        if self.isOpen() == False: # False for closed door, True for open door 
            print(f'{self.name} is already closed')
            return 
        
        if self.open_override.flag is True: 
            self.servo.throttle = self.stop_speed 
            print(f'close {self.name} stopped due to override! Opening door now.')
            self.open_door() 
            return 
        
        start = time.time()
        self.servo.throttle = self.close_speed
        print('isOpen: ', self.isOpen())
        print('time: ', time.time()-start)

        while self.isOpen() and time.time()-start < TIMEOUT:  
            
            if self.open_override.flag is True: 
                self.servo.throttle = self.stop_speed 
                print(f'close {self.name} stopped due to override! Opening door now.')
                self.open_door() 
                return 
            else: 
                time.sleep(0.005)

            #if not GPIO.input(self.state_switch.number): 
                # door shut successfully, stop the door 
                # self.open = False 
            #    self.servo_door.throttle = self.continuous_servo_speed['stop'] # might not need this line here.
                
        self.servo.throttle = self.stop_speed
        # check the reason for exiting the while loop: (either door actually closed, or reached timeout)
        if self.isOpen() is False: # door successfully closed 
            print(f'{self.name} should be closed now! ')
        else: 
            print(f'ah crap, door {self.name} didnt close!') 
        return   
        
                #if not self.door_override[door_ID]:
                # self.servo.throttle = self.continuous_servo_speed['close'] # QUESTION/TODO: why do we have to continuously set this ?? can this go outside of the while loop? 
                #we will close the door until pins for door close are raised, or until timeout
                # if not GPIO.input(pins[f'{door_ID}_state_switch']): # QUESTION/TODO: what is this line checking for??                 

    
    def monitor_override_buttons(self): 
        '''monitor pins for override open and override close'''
        # NOT IN USE RIGHT NOW! 
        while not self.stop_threads: 
            #pullup swtich pins will be 0/False when pressed
            if self.open_override.flag is True: 
                self.open_door() 
                self.open_override.flag = False # reset flag 
            

            if self.close_override.flag is True: 
                self.close_door() 
                self.close_override.flag = False # reset flag 
            
            time.sleep(0.025)
        

                
            '''if GPIO.input(self.override_open_pin) == False: 
                self.close_override = True 
                self.servo_door.throttle = self.close_speed
            else:
                self.close_override = False
                self.servo_door.throttle = self.stop_speed
            
            #this might not really matter, but good to address the case anyway
            if GPIO.input(self.override_open_pin) == False and GPIO.input(self.override_open_pin) == False: 
                self.servo_door.throttle = self.stop_speed'''
        
        # When stop threads is set to true, signal the button threads to stop monitoring as well 
        self.open_override.stop_monitoring() 
        self.close_override.stop_monitoring() 

            
    def cleanup(self): 
        # QUESTION: should we ensure doors are open and/or closed when we finish?? 

        # stop monitoring button presses (threads that are monitoring this finish last round of function and exit)
        self.stop_threads = True 
        #self.open_override.stop_monitoring()
        #self.close_override.stop_monitoring()
        '''if self.isOpen(): 
            self.close_door()'''

        if self.isOpen(): 
            self.close_door() 
        # self.stop_threads = True 

        # emergency stop: 
        self.servo.throttle = self.stop_speed  # force shutoff if any servos are left moving
        
        # self.t1.join()
        # self.t2.join()
        
    
             

    
        

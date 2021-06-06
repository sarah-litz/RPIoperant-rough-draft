''' ----------------------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Hardware.py
                                    description: all of the necessary functions for running the operant pi boxes
-------------------------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# standard lib imports 
import time

# third party imports 
import pigpio 
import RPi.GPIO as GPIO
from gpiozero import LED 
from adafruit_servokit import ServoKit

# local imports 
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
import class_definitions.hardware_classes.lever as Lever # Lever class 

kit = ServoKit(channels=16)
GPIO.setmode(GPIO.BCM) # set up BCM GPIO numbering 
GPIO.setup(25, GPIO.IN) # set GPIO 25 as input 


class Pin(): # class for a single pin 
    def __init__(self, pin_name, pin_number, pin_type): 
        
        self.key = pin_name
        self.number = pin_number
        self.type = pin_type
        self.type_instance = None
        
        self.setup()
    
    def setup(self): # setup with GPIO and create new instance based on type where necessary. (accessed thru self.type_instance)
        
        if 'lever' in self.key or 'switch' in self.key:
            print(self.key + ": IN")
            GPIO.setup(self.number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # LEVER TYPE: lever_IDs can be "food", "door_1", or "door_2"   
            self.type_instance = Lever(self.key) # create Lever Instance 
            
        elif 'read' in self.key:
            print(self.key + ": IN")
            GPIO.setup(self.number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        elif 'led' in self.key or 'dispense' in self.key :
            GPIO.setup(self.number, GPIO.OUT)
            GPIO.output(self.number, 0)
            print(self.key + ": OUT")
        else:
            GPIO.setup(self.number, GPIO.OUT)
            print(self.key + ": OUT") 
            
                    
def setup_pins(pin_dict=None): 
    ''' called from ScriptClass.py during script setup. this returns the initalized pin_obj_dict which contains (pin_name->pin_class_instance) pairs '''
    # function accepts optional argument: user can choose to pass in their own pin dictionary, otherwise the default pins (defined in operant_cage_settings_default.py) are used 
    
    
    if (pin_dict==None): # check if user passed in argument. If not, assign pin_dict to the default values. 
        pin_dict = default_operant_settings.pins
    
    # create new dictionary where each element is (pin_name:Pin_class_instance)
    pin_obj_dict= {} # inialize empty dict
    
    # set the type of the pin based on the pin's name, and then create instance of Pin and append this to pin_obj_dict
    for key in pin_dict.keys(): 
        type = None # reset type to None each iteration
        if 'lever' in key or 'switch' in key:
            # LEVER TYPE: lever_IDs can be "food", "door_1", or "door_2"  
            type = 'lever'
        elif 'read' in key:
            type = 'read'
        elif 'led' in key or 'dispense' in key :
            type = 'led' 
        else:
            pass 
        pin_obj_dict[key] = Pin( key, pin_dict.get(key), type ) # key -> Pin pair added to dictionary
    
    print("initialized pin_obj_dict. To access a single pin object by it's name, use pin_obj_dict['name_of_pin']")
    return pin_obj_dict  
    
        
  
  
                    
def reset_doors(pins):

    #check if the doors are open
    door_state = [False, False]
    if not GPIO.input(pins['door_1_state_switch']):
        print('door1 is open')
        door_state[0] = True

    if not GPIO.input(pins['door_2_state_switch']):
        print('door2 is open')
        door_state[1] = True 
        
    #get the open doors (door_state == False)
    open_doors = [id for id in [0,1] if door_state[id]]

    for door_ID in open_doors:
        start = time.time()


        while not door_state[door_ID] and time.time()-start < 10:
                #if not self.door_override[door_ID]:
                # servo_dict[door_ID].throttle = continuous_servo_speeds[door_ID]['close']

                #we will close the door until pins for door close are raised, or until timeout
                if not GPIO.input(pins[f'{door_ID}_state_switch']):
                    door_state[door_ID] = True
                    servo_dict[door_ID].throttle = continuous_servo_speeds[door_ID]['stop']
                    print("i was here")

        if not door_state[door_ID]:
            print(f'ah crap, door {door_ID} didnt close!') 



''' def open_door(args, pins):
    # open a door!
    door_ID = args

    #double check the right number of args got passed
    if type(door_ID) is tuple:
        if len(door_ID) == 1:
            door_ID = door_ID[0]
        else:
            print(f'yo! you passed close_door() too many arguments! should get 1 (the door_ID), got {len(door_ID)}')
            raise

    self.timestamp_queue.put('%i, %s open begin, %f'%(self.round, door_ID, time.time()-self.start_time))
    servo_dict[door_ID].throttle = continuous_servo_speeds[door_ID]['open']
    open_time = continuous_servo_speeds[door_ID]['open time']
    start = time.time()

    while time.time() < ( start + open_time ) and not self.door_override[door_ID]:
        #wait for the door to open
        time.sleep(0.05)

    #door should be open!
    servo_dict[door_ID].throttle = continuous_servo_speeds[door_ID]['stop']

    print('exiting door open attempts')

    
    if not GPIO.input(pins[f'{door_ID}_state_switch']):
        if self.door_override[door_ID]:
            print(f'open {door_ID} stopped due to override!')
        print(f'{door_ID} failed to open!!!')
        self.timestamp_queue.put('%i, %s open failure, %f'%(self.round, door_ID, time.time()-self.start_time))
    else:
        self.timestamp_queue.put('%i, %s open finish, %f'%(self.round, door_ID, time.time()-self.start_time))
        self.door_states[door_ID] = False
    self.do_stuff_queue.task_done() '''



# set_pins()

''' class RPI: # used to startup the raspberry pi and begin/monitor overall interactions, that aren't specific to a single pin
    def __init__(self): 
    def setup_pins: 
        # make 20 instances of class Pin
'''

''' class Pin: # each pin gets a corresponding instance of Pin. Used to interact with the specific pin. 
    def __init__(self):
        # set as IN or OUT  
        self.name = <function that assigns a more user friendly name to the pin>
        self.type =  lever, led, override_open_switch, overrride_close_switch, 
'''



''' class Servo(Pin(???)): # should get "assigned" to a corresponding pin  
    def __init__(self, type):
        if type == lever: 
            self.lever_angle 
            self.continuous_servo_speed
            self.servo_dict 
'''
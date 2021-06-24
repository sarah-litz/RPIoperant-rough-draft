
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.Pin import Pin
import time
import threading

# constants 
TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 

# globals 
lock = threading.Lock()
''' Lever contains functions that both Door and Food need '''

class Lever(Pin): 
    # LEVER TYPE: lever_IDs can be "food", "door_1", or "door_2" 
    # CONTROLLED BY SERVOS ( accessed thru servo_dict in original code )

    def __init__(self, pin_name, pin_number): 
        super().__init__(pin_name, pin_number) # inherits self.name and self.number from Pin  
        
        self.servo_lever = self.set_servo()
        self.angles = self.set_lever_angle() # gets set in Food.py and Door.py 
        
        # self.continuous_servo_speed = self.set_continuous_servo_speed()
       
        
    ''' ------------- Private Methods -------------- '''
    def set_lever_angle(self):     
         
        if 'food' in self.name: 
            return default_operant_settings.lever_angles.get('food')
        elif 'door_1' in self.name: 
            return default_operant_settings.lever_angles.get('door_1')
        elif 'door_2' in self.name: return default_operant_settings.lever_angles.get('door_2')
        else: pass 
        
        
    '''def set_continuous_servo_speed(self):
        
        if 'food' in self.name: 
            return default_operant_settings.continuous_servo_speeds.get('dispense_pellet')
        elif ('door_1' in self.name): 
            return default_operant_settings.continuous_servo_speeds.get('door_1') 
        elif 'door_2' in self.name: return default_operant_settings.continuous_servo_speeds.get('door_2')
        else: pass''' 
    
    def set_servo(self): 
        if 'food' in self.name: 
            return default_operant_settings.servo_dict.get(f'lever_food')
        if 'door' in self.name: 
            def get_door_id(name): 
                # if this gets passed "lever_door_1", then the function will just return 'door_1' 
                if 'door' in name: 
                    num_filtered = filter(str.isdigit, name) # filter out non-numeric characters 
                    num = "".join(num_filtered) # merges numbers into one string 
                    return("door_" + num)
            door_id = get_door_id(self.name)
            return default_operant_settings.servo_dict.get(f'lever_{door_id}')
            
        
        
    
    ''' ---------------- Public Methods --------------- '''
    def extend_lever(self): 
        print("(EXTENDING LEVER) lever angle: ", self.angles)
        extend = self.angles[0]
        retract = self.angles[1]
        
        #we will wiggle the lever a bit to try and reduce binding and buzzing
        modifier = 15
        if extend > retract:
            extend_start = extend + modifier
        else:
            extend_start = extend - modifier
        
        self.servo_lever.angle = extend_start 
        time.sleep(0.1)
        self.servo_lever.angle = extend 
    
    def retract_lever(self): 
        print("(RETRACTING LEVER) lever angle: ", self.angles)
        retract = self.angles[1]   
        
        start = time.time() 
        self.servo_lever.angle = retract 
    
    

            
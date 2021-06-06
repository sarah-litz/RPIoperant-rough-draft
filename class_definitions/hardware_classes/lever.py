

class Lever: 
    # LEVER TYPE: lever_IDs can be "food", "door_1", or "door_2" 
    # CONTROLLED BY SERVOS ( accessed thru servo_dict in original code )
    
    def __init__(self, pin_name, lever_angles=None, servo_dict=None, continuous_servo_speed=None): 
        # option to pass in user defined values, otherwise default values from operant_cage_settings_default.py are used
        self.pin_name = pin_name
        self.lever_angle = self.get_lever_angle(lever_angles)
        self.servo_dict = self.get_servo_dict_value(servo_dict)
        self.continuous_servo_speed = self.get_continuous_servo_speed(continuous_servo_speed)
    
    ''' ------------ Private Methods ------------ '''
    '''methods for looking up and setting the pin_name's corresponding values '''
    # using <pin_name> as key, lookup the corresponding values in servo_dict, continuous_servo_speeds, and lever_angles 
    def get_lever_angle(self, lever_angles):     
        if (lever_angles == None): 
            return default_operant_settings.lever_angles.get(self.pin_name)
        else: return lever_angles
            
    def get_servo_dict_value(self, servo_dict): 
        if (servo_dict == None): 
            return default_operant_settings.servo_dict.get(self.pin_name)
        else: return servo_dict
        
    def get_continuous_servo_speed(self, continuous_servo_speed):
        if (continuous_servo_speed == None):
            return default_operant_settings.continuous_servo_speeds.get(self.pin_name)
        else: return continuous_servo_speed


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
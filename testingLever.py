import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.DoorLever import (Door) # Lever class 
from class_definitions.hardware_classes.pins_class.FoodLever import (Food) # Lever class 
from class_definitions.hardware_classes.pins_class.Pin import (Pin) # Lever class 

from adafruit_servokit import ServoKit
import os

kit = ServoKit(channels=16)


# extend lever test 
name = 'door_1' # THERE IS NO PIN NAMED 'DOOR_1' SO ISSUES ARE CAUSED 
number = default_operant_settings.pins.get(name)
myLever = Food(name, number)
css = {'stop':0.1, 'close':-0.1, 'open':0.8,
                        'open time':1.6,
                        }
print(css['open'])
myLever.extend_lever()

# close door test 
servo_dict = {'lever_food':kit.servo[14], 'dispense_pellet':kit.continuous_servo[1],
                'lever_door_1':kit.servo[2], 'door_1':kit.continuous_servo[0],
                'lever_door_2':kit.servo[12],'door_2':kit. continuous_servo[13]}

servo_dict['door_1'].throttle = -0.1



name = 'door_1_state_switch'
number = default_operant_settings.pins.get(name)
myStateSwitch = Pin(name, number)

myLever.close_door(myStateSwitch)




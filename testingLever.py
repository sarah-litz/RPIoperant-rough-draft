import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.pins_class.DoorLever import (Door) # Lever class 

name = 'lever_door_1'
number = default_operant_settings.pins.get(name)
myLever = Door(name, number)
css = {'stop':0.1, 'close':-0.1, 'open':0.8,
                        'open time':1.6,
                        }
print(css['open'])
myLever.open_door()



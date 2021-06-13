import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.hardware_classes.lever import (Lever) # Lever class 


myLever = Lever('door_1')
css = {'stop':0.1, 'close':-0.1, 'open':0.8,
                        'open time':1.6,
                        }
print(css['open'])
myLever.open_door()



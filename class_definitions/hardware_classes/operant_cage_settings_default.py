from adafruit_servokit import ServoKit
import os

kit = ServoKit(channels=16)

'''dont change these default values! if you need to make changes to the operant cage settings,
like changing lever angle values or servo speeds, copy '''

if not os.path.isfile('/etc/RPI_operant/operant_cage_settings_local.py'):
    print('no local operant cage settings, reverting to defaults')
    pins = {'lever_food':27,
        'lever_door_1':18,
        'lever_door_2':22,
        'led_food':19,
        'read_pellet':16,
        'speaker_tone':21,
        'led_social':20,
        'door_1_override_open_switch':25, # original: 24
        'door_2_override_open_switch':5, # original: 6
        'door_1_override_close_switch':24, # original: 25
        'door_2_override_close_switch':6, # original: 5
        'door_1_state_switch':4,
        'door_2_state_switch':17, 
        'read_ir_1':12,
        'read_ir_2':13,

        'gpio_sync':23, }


    #values Levers [extended, retracted]
    lever_angles = {'food':[40, 123], 'door_1':[15,98], 'door_2':[45,131]}


    continuous_servo_speeds = {
                            'dispense_pellet':{'stop':0.15, 'fwd':0.12},
                            'door_1':{'stop':0.13, 'close':-0.1, 'open':0.8,
                            'open time':1.6,
                            },
                            'door_2':{'stop':0.15, 'open':-0.1, 'close':0.8,
                            'open time':1.6,
                            }
                                                                                }


    servo_dict = {'lever_food':kit.servo[14], 'dispense_pellet':kit.continuous_servo[1],
                    'lever_door_1':kit.servo[2], 'door_1':kit.continuous_servo[0],
                    'lever_door_2':kit.servo[12],'door_2':kit. continuous_servo[13]}

else: 
    print('importing local operant cage settings')
    import importlib.util
    spec = importlib.util.spec_from_file_location("operant_cage_settings_local", 
                                                    "/etc/RPI_operant/operant_cage_settings_local.py")
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    pins = foo.pins
    lever_angles = foo.lever_angles
    print(lever_angles)
    continuous_servo_speeds = foo.continuous_servo_speeds
    servo_dict = foo.servo_dict 

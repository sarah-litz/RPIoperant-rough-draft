onPressEvents = [
    'script.pulse_sync_line(length=0.25)', 
    "script.buzz(buzz_type='pellet_buzz')",
    'time.sleep(1)', 
    'script.dispense_pellet()', 
    'time.sleep(1)',         
    "script.pins['lever_food'].retract_lever()", 
]

noPressEvents = [
    'script.pulse_sync_line(length=0.25)', 
    "script.buzz(buzz_type='pellet_buzz')", 
    'time.sleep(1)', 
    'script.dispense_pellet()', 
    'time.sleep(1)',         
    "script.pins['lever_food'].retract_lever()", 
]

def fun(): 
    print("hello, there!")
    return 




def configure_callback_events(onPressEvents): 
    def get_arguments(eventString): 
        start = eventString.index('(')
        end = eventString.index(')')
        args = eventString[start+1:end]
        return args 

    def get_arg_val(key, argStr): 
        if 'length' in argStr: 
            keyStart = argStr.index(key + '=')
            start = keyStart + len(key + '=')
            argVal = argStr[start+1:]
            print(argVal)
            return argVal
        else: 
            return None

    onPressFunctions = []
    for func in onPressEvents: 
        if 'pulse_sync_line' in func: 
            args = get_arguments(func)
            print(args)
            keywords = ['length']
            for key in keywords: 
                argVal = get_arg_val(key, args)
                if argVal is not None: 
                    try: 
                        argNum = float(argVal)
                        func = lambda: script.pulse_sync_line(length = argNum)
                    except ValueError: 
                        print("cannot convert arg to a number")
                



configure_callback_events(onPressEvents)
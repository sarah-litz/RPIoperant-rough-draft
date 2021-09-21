''' ----------------------------------------------------------------------------------------------------------------------------------------------
                                                            filename: Lever.py
                            description: Lever Objects are sublcass of Pin Objects. These are instantiated during pin_setup (in ScriptClass.py)
                            Gives access to functions that only apply to Levers including extending/retracting levers, and monitoring the Levers for presses. 
-------------------------------------------------------------------------------------------------------------------------------------------------'''
#!/usr/bin/python3

# local imports
# standard lib imports 
import traceback
import time
import threading
from queue import Queue
import logging
import inspect

# third party imports 
import RPi.GPIO as GPIO

# Globals and Constants 
TIMEOUT = 10 # wait 10 seconds for certain action to happen, and then bail if it did not complete 
lock = threading.Lock()


''' Lever contains functions that both Door and Food need '''

class Lever(): 
    # LEVER TYPE: lever_IDs can be "food", "door_1", or "door_2" 
    # CONTROLLED BY SERVOS ( accessed thru servo_dict in original code )

    def __init__(self, lever_dict, timestamp_q):

        self.name = lever_dict['name']
        self.type = 'Lever'
        self.servo = lever_dict['servo']
        self.extended = lever_dict['extended']
        self.retracted = lever_dict['retracted']
        self.pin = lever_dict['pin']
        
        self.timestamp_q = timestamp_q

        self.all_lever_presses = 0 # num of all presses (including outside of designated timeframe)
        self.monitoring = False 
        self.stop_threads = False 

        self._gpio_setup_pin()
        

    def _gpio_setup_pin(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    ''' ---------------- Public Methods --------------- '''
    def extend_lever(self): 
        
        extend = self.extended
        retract = self.retracted
        #we will wiggle the lever a bit to try and reduce binding and buzzing
        modifier = 15
        if extend > retract: extend_start = extend + modifier
        else: extend_start = extend - modifier
        
        
        self.servo.angle = extend_start 
        timestamp = time.time()
        time.sleep(0.1)
        self.servo.angle = extend 
        self.timestamp_q.put_item(timestamp, f'({self.name} lever) Lever Extended')
        return f'{self.name} lever extended', timestamp, True
        
    def retract_lever(self):         
        timestamp = time.time() 
        self.servo.angle = self.retracted 
        self.timestamp_q.put_item(timestamp, f'({self.name} lever) Lever Retracted')
        return f'{self.name} lever retracted', timestamp, True 
    
    def execute_callback_funcs(self, isPress): 
        if isPress is True: 
            callback_funcs = self.onPressEvents 
        else: 
            callback_funcs = self.noPressEvents

        for func in callback_funcs: 
            try: func() 
            except (NameError): 
                print(f"Name of func ({func}) not recognized")
            # except (TypeError): 
            #    print(f"type error ({inspect.stack()[0][3]}, {inspect.stack()[1][3]})")

    def wait_for_n_presses(self, required_presses): 
        
        start_time = time.time() 
        presses = 0 

        GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=500)
        while (presses < required_presses and time.time()-start_time <  self.press_timeout): 
            if GPIO.event_detected(self.pin): 
                presses += 1
            else: time.sleep(0.025) 
        GPIO.remove_event_detect(self.pin)

        # check reason for breaking out of while loop 
        if presses >= required_presses: 
            print("presses:", presses, "   required_presses:", required_presses)
            timestamp=time.time()
            self.timestamp_q.put_item(timestamp=timestamp, event_descriptor=f'{presses} Presses Detected ({self.name} lever)')
            print(f'{presses} lever presses were detected for {self.name}')
            self.execute_callback_funcs(isPress=True)
            return 'Lever Presses', timestamp, True 
        else: 
            print(f'{self.name} did not detect enough presses within {self.press_timeout} seconds. Detected {presses} out of the required {required_presses} presses.')
            self.execute_callback_funcs(isPress=False)
            return 'Lever Presses', time.time(), False
                

    '''def monitor_lever(self, press_timeout, required_presses=1): 
        # sets required attributes and signals monitor_lever_continuous to call monitor_lever_timeframe 
        self.required_presses = required_presses # set the number of presses that vole must perform to trigger reward
        self.press_timeout = press_timeout # num of seconds vole has to press lever 
        self.monitoring = True # signals the Lever Monitoring Thread that we are now in timeframe where we want vole to make a lever press. 
        print(f"Setting {self.name} lever monitoring to True")
       

    def monitor_lever_continuous(self, onPressEvents, noPressEvents, callback_func): 
        print('MONITOR LEVER CONTINUOUS')
        # rn, callback function is always script.lever_event_callback
        # purpose is to have a constant monitoring of any presses that occur on the lever. 
        # TODO/QUESTION: i am unclear on what I should be doing with this collected information?? so for now I am just gonna let it sit in a queue 
        GPIO.add_event_detect(self.pin, GPIO.RISING, bouncetime=500)
        print(f'starting background thread running to look for events at {self.name}')
        
        while self.stop_threads is False: 
             
            if self.monitoring is False: 
                if GPIO.event_detected(self.pin): 
                    logging.debug('lever press outside of designated timeframe')
                    self.all_lever_presses.append('lever press outside of designated timeframe', time.time())
                    
            else: 
                logging.debug(f'{self.name} monitoring was set to True. Waiting to see if there is a lever press...')
                event_name, timestamp = self.monitor_lever_timeframe() 
                if event_name: 
                    self.all_lever_presses.append(event_name, timestamp) # if event, add to queue of all lever presses
                    events = onPressEvents
                else: 
                    events = noPressEvents
                for func in events: 
                    print(f"CALLING A CALLBACK FUNC: {func}")
                    try: func()
                    except (NameError): 
                        print(f"Name of func ({func}) not recognized")
                    except (TypeError): 
                        print("type error")
                    
                callback_func(self.name, event_name, timestamp) # Callback function (lever_event_callback in ScriptClass.py)
                
                self.monitoring = False # monitoring should never happen for more than 1 iteration in a row, so we set to False. 

            time.sleep(0.025)
        
        GPIO.remove_event_detect(self.pin) # This statement will execute during cleanup() 
        print(f'ending thread to look for events at {self.name}')

    def monitor_lever_timeframe(self): 
        
        logging.debug(f'monitor_lever_timeframe called, now in designated timeframe of waiting for {self.required_presses} presses at {self.name}')
        start = time.time()
        presses=0

        while True: # loops until an event is detected or we reach timeout 
                        
            if GPIO.event_detected(self.pin): # monitor for if vole presses the food lever 
                timestamp = time.time()
                presses+=1
                # self.lever_press_queue.put(time.time())
                if presses == self.required_presses: # TODO/QUESTION: should there be room for error here?? i.e. >= press_num instead of == press_num
                    self.pin_event_queue.put(f'{self.required_presses} lever presses')
                    print(f'{self.required_presses} lever presses were detected')
                    return f'{self.name} lever press', timestamp    
            
            if time.time() - start > self.press_timeout:
                print(f'no press detected at {self.name}.')
                return False, time.time()
            
            time.sleep(0.025) '''      



    ''' Cleanup and Reset functions '''    
    '''def reset(self): 
        # Values that are reset every round 
        self.stop_threads = False # used in continuous monitoring 
        # self.event_count = 0 # incremented each time an event is counted. This should get reset each new round. 
        # self.press_timeout = 0 
        # self.required_presses = 1
        self.monitoring = False
        # self.onPressEvents.clear()'''

            
    def cleanup(self): 
        '''print("All Lever Presses: ") 
        for press in self.all_lever_presses: 
            print(press)'''
        self.stop_threads = True # forces threads that are monitoring a lever to complete
        # print(f'I recorded a total of {len(self.all_lever_presses)} lever presses for {self.name}')
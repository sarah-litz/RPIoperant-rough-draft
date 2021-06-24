#!/usr/bin/python3

import pigpio 
import RPi.GPIO as GPIO
from gpiozero import LED, Button 
from adafruit_servokit import ServoKit

import threading # https://docs.python.org/3/library/threading.html
from queue import Queue # https://docs.python.org/3/library/queue.html#module-queue
import time
import signal
import traceback, sys
import os 
import pandas as pd
import logging


# third party imports 
from adafruit_servokit import ServoKit

# local imports  
from class_definitions.hardware_classes.pins_class.Lever import Lever # import pin class
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.results import Results # manages output data 

# Global Vars 
lever_q = Queue()
event_queue = Queue()
lock = threading.Lock()
event_lock = threading.Lock()

def setup_results(): 
    # prompt user for experiment input 
    print('welcome\n')
    inputfp = 'default.csv'
    outputdir = ('defaultfp')
    print("input filepath:", inputfp)
    print("output directory:", outputdir)
    inputdf = pd.read_csv(inputfp) 
    csv_row = inputdf.loc[1] # get 1st row 
    return Results(csv_row, outputdir)



def setup_lever(): 
    # Create the levers that we are wanting to moitor concurrently: 
    name1 = 'lever_door_1' 
    number1 = default_operant_settings.pins.get(name1)
    myLever1 = Lever(name1, number1)
    
    name2 = 'lever_door_2'
    number2 = default_operant_settings.pins.get(name2)
    myLever2 = Lever(name2, number2)
    
    name3 = 'lever_food'
    number3 = default_operant_settings.pins.get(name3)
    myLever3 = Lever(name3, number3)

    return myLever1, myLever2, myLever3


def monitor_event_queue(results): # TODO: def getting stuck somewhere with this thread
    # thread that waits for stuff to get added to queue and if something is there, it will write to results file.
    # TODO/LEAVING OFF HERE 
    
    while True: 
        event_lock.acquire()
        event = results.event_queue.get()
        event_lock.release()
        print('what the fuck')
        logging.debug('i am monitoring the event queue mmkay')
        results.record_event(event)
        results.event_queue.task_done()
    
    
    
   
def monitor_lever(q, results): 

    lock.acquire() # ** note lock aquire and release are atomic operations 
    lever = lever_q.get() 
    lock.release()
    
    # call detect event for the lever 
    lever.extend_lever()
    
    event_timestamp = lever.detect_event(3)
    if event_timestamp is not False: 
        # event detected for current lever, add to event_queue and flag the event object to let writer thread know 
        results.event_queue.put((lever.name, event_timestamp))
        
    time.sleep(0.3) # force pause before retracting lever cuz it scares me evertime w/out it.   
    lever.retract_lever()
    lever_q.task_done()
    logging.debug('exiting monitor lever function')
    return 



def main(): 
    
    results = setup_results()
    my_levers = setup_lever()
    print(my_levers)
    
    # TODO: signal handler 

    # Worker Thread Pool: 
    for i in range(4):  # creates 4 worker threads 
        threading.Thread(target=monitor_lever, args=(lever_q, results,), daemon=True).start()
        
    # send task requests to the worker thread
    for item in my_levers:
        lever_q.put(item)
    print('All task requests sent\n', end='')

    
    # writer thread 
    threading.Thread(target=monitor_event_queue, args=(results,), daemon=True).start()
    
    # block until all tasks are done
    lever_q.join()
    results.event_queue.join()
    # block until all events are written to file 
    # results.cleanup()
    # results.event_queue.join()

    print('All work completed')
    return 
            
     
     
       
    
try: main()
except KeyboardInterrupt: 
    print("keyboard interrupt detected, shutting down.")
except Exception: 
    traceback.print_exc(file=sys.stdout)
# TODO: add clean up function call here!! Ensures that operant box doesn't get stuck running. (i.e. prevent a servo from endlessly spinning)
sys.exit(0)

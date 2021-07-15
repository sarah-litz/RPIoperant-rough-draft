#!/usr/bin/python3

import pigpio 
import RPi.GPIO as GPIO
from gpiozero import LED, Button 
from adafruit_servokit import ServoKit

import threading # https://docs.python.org/3/library/threading.html
from queue import Queue, Empty # https://docs.python.org/3/library/queue.html#module-queue
import time
import signal
import traceback, sys
import os 
import pandas as pd


# third party imports 
from adafruit_servokit import ServoKit

# local imports  
from class_definitions.hardware_classes.pins_class.Lever import Lever # import pin class
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.Results import Results # manages output data 


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
# Global Vars 
q = Queue()
event_queue = Queue()
event = threading.Event()
lock = threading.Lock()
event_lock = threading.Lock()


def setup_results(): 
    # prompt user for experiment input 
    print('welcome\n')
    inputfp = 'default.csv'
    outputdir = 'defaultfp'
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




def write_results(e, results): 
    
    while threading.main_thread().is_alive(): # continue to loop while main thread is still running 
        logging.debug('write results function looping')
        '''event_is_set = e.wait()
        logging.debug('event set: %s', event_is_set)'''
        # if event_is_set: # an event was recorded in the event_queue
            # send results to output file! 
        results.write_results()
    
    logging.debug('main thread has made its exit, finishing up with writes real quick....')
    # results.cleanup()
    logging.debug('all results have been written, writer thread exiting now.')
    # when exits while loop because main thread has exited,do something with stuff in event_queue that was not written. 
    return 
    
def monitor_lever(q, results): 
    
    lock.acquire() # ** note lock aquire and release are atomic operations 
    try: 
        lever = q.get(timeout=5) # if no levers have been added to queue after 5 seconds
    except Empty: 
        lock.release()
        logging.debug('lever queue emtpy, exiting monitor lever now')
        return
    
    lock.release()
    
    lever.extend_lever()
    
    # call detect event for the lever 
    event_timestamp = lever.detect_event(3)
    if event_timestamp: 
        # event detected for current lever, add to event_queue and flag the event object to let writer thread know 
        results.event_queue.put([lever.name, event_timestamp])
        # QUESTION/TODO: OR CAN I JUST DIRECTLY WRITE THE EVENT TO OUTPUT FILE? 
        # results.record_event(lever.name, event_timestamp)

        
        time.sleep(0.3) # force pause before retracting lever cuz it scares me evertime w/out it.   
        
            
    '''event_lock.acquire()
        event.set() 
        event_lock.release()'''
    '''if event_queue is Empty: 
        event_lock.acquire()
        event.clear() # reset event flag to False until a diff event is detected 
        event_lock.release()''' 
    
    q.task_done()
    lever.retract_lever()
    logging.debug('exiting monitor lever function')
    return 


def main(): 
    
    results = setup_results()
    my_levers = setup_lever()
    print(my_levers)
    
    # TODO: signal handler 
    
    # Worker Thread Pool: 
    for i in range(4):  # creates 4 worker threads 
        threading.Thread(target=monitor_lever, args=(q, results), daemon=True).start()
        
    # send task requests to the worker thread ( adding levers that need to be monitored )
    for item in my_levers:
        q.put(item)
    print('All task requests sent\n', end='')

    # writer thread 
    threading.Thread(target=write_results, args=(event, results)).start() # QUESTION: should this be daemon thread? I'm thinking no to ensure that data is not lost.
    
    # block until all levers have finished monitoring are done
    q.join()
  
    '''print('All work completed')
    if threading.active_count is 0: 
        print('no more active threads')
        exit()'''
    
    # logging.logThreads()
            
     
     
       
main()   
try: main()
except KeyboardInterrupt: 
    print("keyboard interrupt detected, shutting down.")
except Exception: 
    traceback.print_exc(file=sys.stdout)

# TODO: add clean up function call here!! Ensures that operant box doesn't get stuck running. (i.e. prevent a servo from endlessly spinning)
GPIO.cleanup()
sys.exit(0)

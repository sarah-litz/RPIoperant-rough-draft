''' 

Note on how to run this file: 
> python doesn't like the imports in this file since we are running this file in a subdirectory, so it doesn't know the other subdirectories exist. 
As a work around, to run this file run it from the root 'RPIoperant-rough-draft' directory, and use the following command: 

/RPIoperant-rough-draft $ python3 -m Threading.lever_press_threading.py  

'''

#!/usr/bin/python3

# standard lib imports 
import threading # https://docs.python.org/3/library/threading.html
from queue import Queue # https://docs.python.org/3/library/queue.html#module-queue
import time
import signal
import traceback, sys



# third party imports 
from adafruit_servokit import ServoKit

# local imports  
from class_definitions.hardware_classes.pins_class.Lever import Lever # import pin class
import class_definitions.hardware_classes.operant_cage_settings_default as default_operant_settings
from class_definitions.Results import Results # manages output data 


# Global Vars 
q = Queue()
lock = threading.Lock()
exit_event = threading.Event()
kit = ServoKit(channels=16)


###### myThread class thing is not in use right now....
# https://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
class myThread(threading.Thread): # creating a subclass of threading.Thread
    def __init__(self, pool): 
        threading.Thread.__init__(self)
        self.pool = pool
    def run(self): 
        try: 
            raise Exception('an error occured here.')
        except Exception: 
            self.bucket.put(sys.exc_info())
######



def setup_result(): 
    output = Results('default.csv', )
    
    
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



def monitor_lever(lever): 
    # call detect event for the lever 
    lever.extend_lever()
    lever.detect_event(6) # the number 4 says wait 4 seconds before timeout
    lever.retract_lever()
    
def worker(q,):
    while True:
        # acquire lock before getting item from queue to ensure that threads don't get same item
        
        lock.acquire() # ** note lock aquire and release are atomic operations 
        item = q.get()
        lock.release()
        
        print(f'{threading.get_ident()} is working on {item.name}')
        # work goes in here 
        
        monitor_lever(item)
        
        print(f'Finished {item.name}')
        print(f'done monitoring {item.name}')
        q.task_done()
        


def main(): 
        
    my_levers = setup_lever()
    print(my_levers)
    
    # TODO: signal handler 
    
    # Worker Thread Pool: 
    for i in range(4):  # creates 4 worker threads 
        threading.Thread(target=worker, args=(q,), daemon=True).start()



    # send thirty task requests to the worker
    for item in my_levers:
        q.put(item)
    print('All task requests sent\n', end='')

    # block until all tasks are done
    q.join()
    print('All work completed')
    if threading.active_count is 0: 
        exit()
            
     
     
       
    
try: main()
except KeyboardInterrupt: 
    print("keyboard interrupt detected, shutting down.")
except Exception: 
    traceback.print_exc(file=sys.stdout)
# TODO: add clean up function call here!! Ensures that operant box doesn't get stuck running. (i.e. prevent a servo from endlessly spinning)
sys.exit(0)



'''
# Create thread pool; here we have 2 worker threads 
t1 = threading.Thread( target = threader, args=() ) # creates new instance of the Thread class 
t2 = threading.Thread ( target = threader, args=() )

t1.daemon = True # ensures that threead will die when the main thread dies 
t2.daemon = True # can set t.daemon to false if you want it to keep running. 

t1.start()
t2.start()

t1.join()
t2.join()

# If we have 4 jobs to be completed, then we will add those jobs to a job queue and the threads will pull off of this queue. 
for job in range(4): 
    q.put(job)


print("Done!")
'''



#!/usr/bin/python3

# standard lib imports 
import threading # https://docs.python.org/3/library/threading.html
from queue import Queue # https://docs.python.org/3/library/queue.html#module-queue
import time


q = Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

# turn-on the worker thread
t1 = threading.Thread(target=worker, daemon=True)
t1.start() 

# send thirty task requests to the worker
for item in range(30):
    q.put(item)
print('All task requests sent\n', end='')

# block until all tasks are done
q.join()
print('All work completed')


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


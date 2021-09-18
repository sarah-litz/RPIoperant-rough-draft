
#!/usr/bin/python3

# standard lib imports 
import time
from queue import Queue 


class Timestamp(): 
    def __init__(self, timestamp, event_descriptor, round): 
        self.timestamp = timestamp
        self.event_descriptor = event_descriptor
        self.round = round 
        


class TimestampQueue(): 
    def __init__(self): 
        self.recorded_items = Queue() 
        # Round and start time are updated each new round 
        self.round = 0 
        self.start_time = time.time() 
    
    def put_item(self, timestamp, event_descriptor): 
        # convert timestamp to time from start of round 
        time_since_round_start = timestamp - self.start_time
        # creates/adds a new Timestamp instance to the TimestampQueue 
        self.recorded_items.put( Timestamp(time_since_round_start, event_descriptor, self.round) ) 
    
    def get_item(self): 
        return self.recorded_items.get()
    def task_done(self): 
        self.recorded_items.task_done() 

    def print_items(self): 
        print('--Timestamp Queue--')
        for q_item in self.recorded_items.queue: 
            print((q_item.timestamp, q_item.event))
        print('----------------')
    
    def finish_writing_items(self): 
        self.recorded_items.join() 
    

    
    

    
    
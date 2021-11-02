
#!/usr/bin/python3

# standard lib imports 
import time
from queue import Queue 




class Phase(): 
    def __init__(self, timestamp_manager, name, length, print_countdown): 
            # if timeframe is None, then there is no time limit on this phase. As a result, it will run until interrupt or a new phase is created
            self.active = True 
            self.name = name 
            self.timestamp_manager = timestamp_manager
            self.timeframe = length
            if print_countdown: self.display_countdown_timer() 
    
    def display_countdown_timer(self): 
        # print a countdown to the screen based on the remaining time left in <timeframe> 
        pass 

class Timestamp(): 
    def __init__(self, timestamp_manager, event_descriptor, timestamp): 
        
        # self.timestamp = "{:.2f}".format(timestamp) # format time to 2 decimal points 
        self.timestamp = timestamp
        self.timestamp_manager = timestamp_manager 
        self.event_descriptor = event_descriptor # string that describes what the event is 
        self.round = timestamp_manager.round # round number that event occurred during 
        self.phase = timestamp_manager.phase
    
    def add_to_queue(self): 
        # self.timestamp = "{:.2f}".format(self.timestamp)
        self.timestamp_manager.record_new(self)
        
        


class TimestampManager(): 
    def __init__(self): 
        self.queue = Queue() 
        # Round and start time are updated each new round 
        self.round = 0 
        self.round_start_time = time.time() 
        self.phase = self.new_phase('Object Instantiation Phase')

    '''# # # # # # # # # # 
    #   Phase Class   # # Wrapping Phase Class into Timestamp Manager to make it clear that Timestamp Manager is in charge of tracking the changes to Phase Info, and sharing that information with other objects/scripts. 
    # # # # # # # # # # 
    class Phase(): 
        def __init__(self, name, timeframe=None):
            # if timeframe is None, then there is no time limit on this phase. As a result, it will run until interrupt or a new phase is created
            self.active = True 
            self.name = name 
            self.timeframe = timeframe '''
    

    # LEAVING OFF HERE!!!! 
    def new_phase(self, name, length=None, print_countdown=True): # creates a new phase, forgetting whatever phase we were previously in
        # self.phase = self.Phase(name, timeframe)
        self.phase = Phase(self, name, length, print_countdown)
        

    def record_new(self, timestamp_obj ): # TIME PHASES? pass phase_number as argument here  
        # convert timestamp to time from start of round 
        time_since_round_start = "{:.2f}".format(timestamp_obj.timestamp - self.start_time)
        # creates/adds a new Timestamp instance to the TimestampQueue 
        self.queue.put(time_since_round_start, timestamp_obj.event_descriptor, timestamp_obj.round)
    
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
    

    
    

    
    
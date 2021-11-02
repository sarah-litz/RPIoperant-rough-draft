from ..class_definitions.ScriptClass import Script


class UserScript(Script): 
    def __init__(self, csv_input, output_dir, key_values): 
        super().__init__(csv_input, output_dir, key_values)

        self.user_script_events = [] # List of lambda functions (similar to onPressEvents, except we will append to the list dynamically)
        self.action_keywords_list = [ # List of valid action words that user can enter into their script 
            'open', 'open door', 
            'close', 'close door', 
            'extend', 'extend lever', 
            'retract', 'retract lever', 
            'wait', 'sleep', 'delay',
            'buzz', 'play sound', 
            'pulse', 'pulse sync line',
            'dispense', 'dispense pellet', 
            'retrieval','pellet retrieval', 
            
            # OnPressEvents
            
        ]

        ''' Read in JSON File that contains the user's script 
            - Validate their entries to make sure it corresponds with an existing object and/or function
            - Once validation has completed, call the specified functions in the given order. 
        '''

        # grab the name of the JSON file that the user specified in a column in csv_input 
        # if JSON file exists, open the file. Else, throw an error and return. 
        # Load in the data from the JSON file. 

        ''' JSON data gets stored in a python dictionary '''
        ''' Validate that what the user entered is a valid function call '''
        # Loop thru the dictionary that contains the JSON data 
        # for each key/value pair: 
            # self.validate(jsonObj, self.user_script_events)
    
        ''' 
        def validate(self, jsonObj, valid_objects_list = self.user_script_events): 

            # Validate by comparing to a list (in this module) that has a list of all of the valid key words that can be used. 
            

                # compare the function key word that the user entered to the list of funcion key words (that we will define in this module). 
                # If it exists, continue to loop. If it does not exist, throw an error/print to screen and return.
                #    
            
            
            if jsonObj.action is in self.keyword_validation_list.keys():
                
                -----
                switch statement with all of the function key words, and inside each switch statement make a function call to the corresponding validation function
                -----
                if jsonObj.action == "open" or "open door": 
                    self.validate_open_door(jsonObj)
                elif jsonObj.action == "buzz": 
                    self.validate_buzz(jsonObj)
                elif jsonObj.action == "on press events" or "on press": 
                    self.validate_onPressEvents(jsonObj)

                ...etc... 
            

            else: 
                throw an error 
                print('invalid action word: {jsonObj.action}')
                return 


            '''

    # # def validate_function_name(self) # # 
    # # validation that is specific to a single function # #
'''
    def validate_open_door(self, jsonObj, valid_objects_list = self.user_script_events)
        vals = self.keyword_validation_list.get(jsonObj.action)

        door_list = self.box.get_object_list(doors): # (add function that returns a list of object. Optional argument to specify if you want a list of only objects of a certain type.)
        if jsonObj.object does not exist in door_list.name: 
            print('invalid door. {jsonObj.object} does not exist.')
            return False
        
        else: 
            # get door_list object where (jsonObj.object == door_list.name)
            doorObj = door_list.get(door_list.name==jsonObj.object) # idk how to do this correctly but the idea is there. 
            
            # Add To the List of Anon Functions that we will eventaully execute! 
            valid_objects_list.append( lambda: doorObj.open_door() )

            # We have now validated and found the object/function for a single JSON command the user specified. Return from this funciton. 
            return True
                
     
'''


'''
    def validate_onPressEvents(self, jsonObj, valid_objects_list = self.user_script_events): 

        # remove the "on press" part of the jsonObj and then reevaluate as any other function that user specified 
        jsonObj.action = jsonObj.argument[1] # this syntax will likely need revising I don't think this will work as is. 
        jsonObj.object = jsonObj.argument[2] 
        valid = self.validate(jsonObj, valid_objects_list = self.onPressEvents ) # validate the function that was specified as being an "on press" function  
        if Valid: 
            return True 
        else: 
            print('invalid onPressEvent specified: {jsonObj}')
            return False 
'''
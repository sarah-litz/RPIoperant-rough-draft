

## Instructions for adding a new version of an experiment. (adding a new run_scripts file)

# 1. create a new file in the folder run_scripts. Must end with '.py' to denote that this is a python file. ( <myFile>.py ) 

# 2. Add a comment that will serve as a header/title to the file. Use the following format: 
            ''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: myFile.py
                    author: < your name >
                    description: < what happens in this file? >
            -----------------------------------------------------------------------------------------------------------------------------------'''

# 3. Copy and paste the following line to the beginning of the file: 

        from run_scripts.Script import Script # import the parent class 


# 4. Copy and paste the following code into your file ( this creates a subclass that allows you to define key_values for your new script ): 
        
        from collections import OrderedDict

        class SubScript(Script):  # subclass of parent class Script (defined in ScriptDriver)
            pass
            # Child class automatically gets Script's methods. If we simply "pass", child function will also automatically get parent's attributes as well. 
                # if we add __init__ to child, however, it does not inherit the parent attributes anymore, it will only inherit the funcitons. 
                # on child inheritance syntax: https://www.w3schools.com/python/python_inheritance.asp
            def __init__(self, key_value_dict):
                super().__init__(key_value_dict) # super() sets it so we inherit parent attributes, and now we are able to alter those attributes as needed.
                print("hello from the child class of Script: MagazineScript")
            
            def setup_keyValues(self): 
                if __name__ == '__main__':
                    '''running directly, user will enter in key values manually'''
                    pass 
                else: 
                    '''use the key values that were initially defined in the __init__ attribute '''
                    




        def setup(): 
            ''' initalize the MagazineScript values, and then create a new instance of MagazineScript which we will return to start()'''
            key_values_dict = OrderedDict.fromkeys(['num_rounds', 'round_time', 'timeII','timeIV']) # fromkeys initializes the vals to common value: in this case sets them to NULL

            # PLACE YOUR KEY VALUES HERE!!! -----------------------------------------------
            # define the values of key_values_dict: 
            key_values_dict['string_to_denote_key_value'] = value
            # -----------------------------------------------------------------------------

            script = SubScript(key_values_dict) # pass the key values to MagazineScript
            return script
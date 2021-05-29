

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
        
        
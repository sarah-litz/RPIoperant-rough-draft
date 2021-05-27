
''' --------------------------------------------------------------------------------------------------------------------------------
                                                    filename: Magazine.py
                    description: 
-----------------------------------------------------------------------------------------------------------------------------------'''

from collections import OrderedDict
from run_scripts.Script import Script # import the parent class 



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

    # define the values of key_values_dict: 
    key_values_dict['num_rounds'] = 2
    key_values_dict['round_time'] = 5 
    key_values_dict['timeII'] = 1 
    key_values_dict['timeIV'] = 2

    script = SubScript(key_values_dict) # pass the key values to MagazineScript
    return script
    
def start():         
    print(' hello from Magainze.py start function ')
    scriptVals = setup() # initalizes instance of MagazineScript with the user defined values for the script 
    print("new script: ", scriptVals)
    print("key values of new script:", scriptVals.key_values)
    
    
    print("Number of Rounds:", scriptVals.key_values['num_rounds'])
    for count in range(0, int(scriptVals.key_values['num_rounds'])): 
        print("round #",count+1)

    return True 
    



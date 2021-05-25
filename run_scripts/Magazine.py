
import sys
from ScriptDriver import Script # TODO/QUESTION: is circular import bad??? 
sys.path.append('run_scripts') # ensures that interpreter will search in this directory for modules 


class MagazineScript(Script):  # subclass of parent class Script (defined in ScriptDriver)
    pass
    # Child class automatically gets Script's methods. If we simply "pass", child function will also automatically get parent's attributes as well. 
        # if we add __init__ to child, however, it does not inherit the parent attributes anymore, it will only inherit the funcitons. 
        # TODO: what is the best structure to keep track of key values? 
            # requirements: ordered, key->value pairs 
            # python's OrderedDict? 
            # on child inheritance syntax: https://www.w3schools.com/python/python_inheritance.asp
    def __init__(self, scriptName):
        super().__init__(scriptName) # super() sets it so we inherit parent attributes, and now we are able to alter those attributes as needed.
        print("hello from the child class of Script: MagazineScript")
    
    def setup_keyValues(self): 
        if __name__ == '__main__':
            '''running directly, user will enter in key values manually'''
            pass 
        else: 
            '''use the key values that were initially defined in the __init__ attribute '''
            pass
        

def start(Script):         
    print(' hello from Magainze.py start function ')
    newScript = MagazineScript(Script)
    print("new script: ", newScript)
    



    print("Number of Rounds:", MagazineScript.get_key_value(newScript, 'num_rounds'))
    #for count in range(0, int(MagazineScript.get_key_value(newScript, 'num_rounds'))): 
    #    print("|")

    return True 
    



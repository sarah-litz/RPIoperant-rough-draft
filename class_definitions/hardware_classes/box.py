import importlib.util
from .Door import Door
from .pins_class.Lever import Lever
from .pins_class.Pellet import Pellet
from .pins_class.Button import Button
from .pins_class.Output import Output
from . import operant_cage_settings_default as default_operant_settings
# import Beam

default_config_file = 'class_definitions/hardware_classes/operant_cage_settings_default.py'
class Box:
    
    def __init__(self, config_file=None):
        
        # Initialize file containing the box values we want to use
        self.config = config_file if config_file else default_config_file
        self.config_name = self.config.split(sep='/')[-1].replace('.py','')
        
        #--------------- get setup information from config file --------#
        spec = importlib.util.spec_from_file_location(self.config_name, 
                                                      self.config)
        self.config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.config_module)

        self.object_list = [] # appends list of all objects for easy cleanup at experiment end 
        #---------------------------------------------------------------#
        
        
        ###############
        for lever in self.config_module.levers:
            new_lever = Lever(lever)
            
            name = new_lever.name+'_lever'
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a lever with that name. Check for duplicate names in the config file')
            
            self.object_list.append(new_lever)
            setattr(self, name, new_lever)


        ###############
        for door in self.config_module.doors:
            new_door = Door(door)
            
            name = new_door.name
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a door with that name. Check for duplicate names in the config file')

            self.object_list.append(new_door)
            setattr(self, new_door.name, new_door)
        
        
        ###############
        for button in self.config_module.buttons: 
            
            new_button = Button(button)

            door_name = new_button.door 
            door = getattr(self, door_name) # get door object 

            function = new_button.function 
            # name = (f'{function}_{door_name}_button')
            name = (f'{function}_button')

            if hasattr(door,name): 
                    raise NameError(f'{door_name} already contains a {name} attribute, but tried to make a button with that name. Check for duplicate names in the config file')

            self.object_list.append(new_button)
            setattr(door, name, new_button)

        ###############
        for dispenser in self.config_module.dispensers:
            new_dispenser = Pellet(dispenser)
            
            name = new_dispenser.name
            
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a dispenser with that name. Check for duplicate names in the config file')
            
            self.object_list.append(new_dispenser)
            setattr(self, name, new_dispenser)


        ###############
        '''for beam in self.config_module.beams:
            new_beam = Beam(beam)
            
            name = new_beam.name
            
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a beam with that name. Check for duplicate names in the config file')
            
            setattr(self, new_beam.name, new_beam)'''


        ###############
        for output in self.config_module.outputs:
            new_output = Output(output)
            
            name = new_output.name
            
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make an output with that name. Check for duplicate names in the config file')
            
            self.object_list.append(new_output)
            setattr(self, new_output.name, new_output)
            
        
        ###############

        
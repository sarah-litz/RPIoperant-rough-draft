import importlib.util
from hardware_classes import Door, Lever, Pellet
import Pellet
import Output
import Door
import Beam

default_config_file = ''
class Box:
    
    def __init__(self, config_file = None):
        
        self.config = config_file if config_file else default_config_file
        self.config_name = self.config.split(sep='/')[-1].replace('.py','')
        
        #--------------- get setup information from config file --------#
        spec = importlib.util.spec_from_file_location(self.config_name, 
                                                      self.config)
        self.config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.config_module)
        #---------------------------------------------------------------#
        
        
        ###############
        for lever in self.config_module.levers:
            new_lever = Lever(lever)
            
            name = new_lever.name+'_lever'
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a lever with that name. Check for duplicate names in the config file')
            
            setattr(self, name, new_lever)


        ###############
        for door in self.config_module.doors:
            new_door = Door(door)
            
            name = new_door.name
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a door with that name. Check for duplicate names in the config file')

            setattr(self, new_door.name, new_door)


        ###############
        for dispenser in self.config_module.dispensers:
            new_dispenser = Pellet(dispenser)
            
            name = new_dispenser.name
            
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a dispenser with that name. Check for duplicate names in the config file')
            
            setattr(self, name, new_dispenser)


        ###############
        for beam in self.config_module.beams:
            new_beam = Beam(beam)
            
            name = new_beam.name
            
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make a beam with that name. Check for duplicate names in the config file')
            
            setattr(self, new_beam.name, new_beam)


        ###############
        for output in self.config_module.outputs:
            new_output = Output(output)
            
            name = new_output.name
            
            if hasattr(self, name):
                raise NameError(f'box already has {name} attribute, but tried to make an output with that name. Check for duplicate names in the config file')
            
            setattr(self, new_output.name, new_output)
            
        
        
        
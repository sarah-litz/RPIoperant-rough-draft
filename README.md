# RPI Operant Code 

# Sarah Notes (TODOs)


## 1. Command Line Arguments 
    - instead of prompting the user one at a time for the input file info and the output file info and stuff, the user can instead just enter these in as command line arguments. 
    - use args parser to accept arguments; this makes the arguments optional. So we need to handle the cases for both when the user does and does not provide an argument. 
    - argument 1 = input file path 
    - argument 2 = output file directory 

## 2. Input File Changes: Mechanism so user is able to change key_values to differ from their default values 

## 3. Output File Changes: 
    - Move the default Output Data File directory to be outside of the /RPI-ROUGHDRAFT file, because we don't want these files to get added to the github repo cause that would get messy really fast. 
    - we also want an option so the user can specify the name of the directory they would like this to be stored at. 
    - we need an ouptut file to be generated for each script run. That is why the user is only specifying the directory name, because then we will autogenerate the output filenames 


## 4. Everytime that an event happens, we want to write to the output file. Ensures that we don't lose any data if something goes wrong in the experiment. 




# RPI Operant Code 

# Sarah Notes (TODOs)


## 1. Command Line Arguments 
    - instead of prompting the user one at a time for the input file info and the output file info and stuff, the user can instead just enter these in as command line arguments. 
    - use args parser to accept arguments; this makes the arguments optional. So we need to handle the cases for both when the user does and does not provide an argument. 
    - argument 1 = input file path 
    - argument 2 = output file directory 

## 2. Input File Changes: Mechanism so user is able to change key_values to differ from their default values 
    - Potential solution: If user wants to change the default key value, they will go into the input csv file and just change the number in that column. 
                            Then, at the end of that experiment being completed, the input csv file is written over to "reset" it with its initial default values. 
                            Unsure of how to deal with the fact that the key_values differ so much between the different script types. 
                            Can I potentially have a column for everything and if a script doesn't use a certain key_value it just leaves that one blank?? 
                            Or, potentially group the key_values into ones that all of them have, and then just add an extra column that mimics the current "change_var" column. 
                            OR... 
                                we keep default_keyValue_dict on hand all the time. 
                                then, use can go into csv file and change the values if they want. 
                                at the start of the experiment, we compare the default key values with the entered key values, and we write to the user to let them know: Here are the values that you have changed away from the default key values (maybe double check that the default vals are correct?), and then we set the script.key_values = changed key values 

                                when all the scripts have finished running, if the user had changed values from their default values, prompt the user with: "do you want to leave the csv file with the changed values? or would you like to reset these values back to their default values?". And if they choose reset values, then write the default_key_values to the input csv file before exiting. 

## 3. Output File Changes: 
    - Move the default Output Data File directory to be outside of the /RPI-ROUGHDRAFT file, because we don't want these files to get added to the github repo cause that would get messy really fast. 
    - we also want an option so the user can specify the name of the directory they would like this to be stored at. 
    - we need an ouptut file to be generated for each script run. That is why the user is only specifying the directory name, because then we will autogenerate the output filenames 


## 4. Everytime that an event happens, we want to write to the output file. Ensures that we don't lose any data if something goes wrong in the experiment. 




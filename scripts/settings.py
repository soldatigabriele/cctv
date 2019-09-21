import os
from dotenv import load_dotenv

load_dotenv()

def get_env_value(envVariable):
    value = os.getenv(envVariable)
    if(value is None or value==""):
        print('Set the ' + envVariable + ' in the .env file')
        exit()
    return value

def get_list_of_files(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        if not entry.startswith("."):
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory 
            if os.path.isdir(fullPath):
                allFiles = allFiles + get_list_of_files(fullPath)
            else:
                allFiles.append(fullPath)
    return allFiles
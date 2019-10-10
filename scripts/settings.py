import os
import logging
import datetime
from dotenv import load_dotenv
from logging.handlers import TimedRotatingFileHandler

# Load the .env file
load_dotenv()

def get_env_value(envVariable):
    value = os.getenv(envVariable)
    if(value is None):
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

# Get the logger
logger = logging.getLogger('logger')

logger.setLevel('DEBUG')
handler = TimedRotatingFileHandler("storage/logs/app.log", when="midnight", interval=1)
handler.suffix = "%Y%m%d"
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S'))
logger.addHandler(handler)

# Create an handler for the console output
c_handler = logging.StreamHandler()
c_handler.setLevel('INFO')
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S'))
logger.addHandler(c_handler)

def log(message, level="debug"):
    if get_env_value("LOG_CHANNEL") in ["console", "test"]:
        print("[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + level.upper() + ": " + message)
    if get_env_value("LOG_CHANNEL") in ["file"]:
        if(level == "error"):
            # exc_info will log the exception details
            logger.error(message, exc_info=True)
            return
        # call the method on logging e.g. logging.info logging.warning etc
        getattr(logger, level)(message)

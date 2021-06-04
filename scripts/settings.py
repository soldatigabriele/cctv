import os
import logging
import datetime
import configparser
from logging.handlers import TimedRotatingFileHandler

# Load the configuration file
configuration = configparser.ConfigParser()
configuration.read('config/config.ini')

def config(key, type = "string"):
    """ Returns the value of the
    configuration passed as key.
    Requires the section.key as format
    """
    keys = str.split(key, ".")
    if type == "bool":
        return configuration[keys[0]].getboolean(keys[1])
    else:
        return  configuration[keys[0]].get(keys[1])

def camera_config(camera, key, type = "string"):
    """Returns the config for a specific
    Camera. Takes the camera number as first
    parameter, the key as second one, and the 
    type as third parameter
    """
    camera = ("Camera-%s" % camera)
    if type == "bool":
        return configuration[camera].getboolean(key)
    else:
        return  configuration[camera].get(key)

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

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
handler = TimedRotatingFileHandler("storage/logs/app.log", when="midnight", interval=1, backupCount=7)
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
    if config("General.LogChannel") in ["console", "test"]:
        print("[" + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + level.upper() + ": " + message)
    if config("General.LogChannel") in ["file"]:
        if(level == "error"):
            # exc_info will log the exception details
            logger.error(message, exc_info=True)
            return
        # call the method on logging e.g. logging.info logging.warning etc
        getattr(logger, level)(message)

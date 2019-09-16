#!/usr/bin/env python3
import subprocess
import os
import main
import time
import shutil
import datetime
import video as videoHelper
from dotenv import load_dotenv

load_dotenv()

def getListOfFiles(dirName):
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
                allFiles = allFiles + getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)
    return allFiles

def moveNewFiles():
    # Current path
    # TODO source = os.getenv("SOURCE_PATH")
    source = os.getcwd() + "/../video/cctv/"
    output_folder = os.getcwd() + "/../video/output/"
    # take the new video and move it to a output folder
    for video in getListOfFiles(source):
        datetime_object = datetime.datetime.now()
        video_folder = output_folder + str(datetime_object.month) + str(datetime_object.day) + str(datetime_object.hour) + str(datetime_object.minute) + str(datetime_object.second) + str(datetime_object.microsecond)
        os.mkdir(video_folder)
        frames_folder = video_folder + "/frames"
        os.mkdir(frames_folder)
        os.rename(video, video_folder + "/video.h264")
        # We have now /output/91520328263175/video.h264
        
        # Instantiate the video helper to extract the frames
        video_helper = videoHelper.Helper
        video_helper.extractFrames(video_helper, video_folder + "/video.h264", frames_folder)
        outcome = False
        for frame in getListOfFiles(frames_folder):
            print("examinating next frame")
            model = main.Predictor
            outcome = model.detect(model, frame, video_folder)
            if outcome:
                print('Person found!')
                person_found = True
                break
            else:
                print('no person found')

        # if outcome is not True, delete the folder with the video and frames
        print("person_found?")
        print(person_found)


while True:
    moveNewFiles()
    time.sleep(4)

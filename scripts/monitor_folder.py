#!/usr/bin/env python3
import subprocess
import os
import main
import time
import shutil
import datetime
import os.path as path
import video as videoHelper
from dotenv import load_dotenv
from notification import notify

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

def getEnvValue(envVariable):
    value = os.getenv(envVariable)
    if(value is None or value==""):
        print('Set the path to the folder you want to monitor in the .env file')
        exit()
    return value

def isFileOlderThanXDays(file, days=1): 
    file_time = path.getmtime(file) 
    # Check against 24 hours 
    if (time.time() - file_time) / 3600 > 24*days: 
        return True
    else: 
        return False

def moveNewFiles():
    # Current path
    source = getEnvValue("SOURCE_PATH")
    output_folder = os.getcwd() + "/../video/output/"
    # take the new video and move it to a output folder
    for video in getListOfFiles(source):
        datetime_object = datetime.datetime.now()
        print("new video found: " + video + " at " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        video_folder = output_folder + str(datetime_object.month) + str(datetime_object.day) + str(datetime_object.hour) + str(datetime_object.minute) + str(datetime_object.second) + str(datetime_object.microsecond)
        os.mkdir(video_folder)
        frames_folder = video_folder + "/frames"
        os.mkdir(frames_folder)
        os.rename(video, video_folder + "/video.h264")
        # We have now /output/91520328263175/video.h264

        # Instantiate the video helper to extract the frames
        video_helper = videoHelper.Helper()
        frames_interval = getEnvValue("FRAMES_INTERVAL")
        video_helper.extractFrames(video_folder + "/video.h264", frames_folder, frames_interval)
        outcome = False
        for frame in getListOfFiles(frames_folder):
            print("examinating: " + frame)
            model = main.Predictor()
            outcome = model.detect(frame, video_folder)
            if outcome:
                print("found person")
                break

        # If the outcome is not True, delete the folder with the video and frames
        if not outcome:
            print('No human found. Removing folder')
            shutil.rmtree(video_folder, ignore_errors=True)

        return outcome
    return None

while True:
    photo = moveNewFiles()
    if photo:
        notify(photo)
    time.sleep(4)

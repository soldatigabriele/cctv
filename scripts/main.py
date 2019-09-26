#!/usr/bin/env python3
import subprocess
import os
import cv2
import time
import shutil
import datetime
from settings import * 
import os.path as path
from model import analyse_image
from video import prepare_video
from notification import *

def process():
    output_folder = os.getcwd() + "/../video/output/"
    # Take the new video and move it to the output folder
    for video in get_list_of_files(get_env_value("SOURCE_PATH")):
        video_folder, frames = prepare_video(video, output_folder)
        # Now that we have extracted the frames from the video, let's start the analysis 
        outcome = False
        for frame in frames:
            print("analysing: " + frame)
            outcome = analyse_image(frame, video_folder)
            if outcome:
                print("object found")
                break

        # If the outcome is not True, delete the folder with the video and frames
        if not outcome:
            print('No object found. Removing folder')
            shutil.rmtree(video_folder, ignore_errors=True)

        return outcome
    return None

# Start the loop
while True:
    try:
        # Analyse the new video
        outcome = process()
        # If the outcome is positive, send a notification
        if outcome:
            notify(outcome)
    except:
        send_message("An error occurred at " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        time.sleep(60)
    time.sleep(1)

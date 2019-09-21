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
from notification import notify

def extract_frames(video_path, output_path, frames_interval = 24):
    vc = cv2.VideoCapture(video_path)
    c=1
    name = 1

    if vc.isOpened():
        rval , frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()
        # Here we set the frames to take (24 means 1 frame every 24, so 1 per second in our stream)
        if c%(frames_interval) == 0 :
            cv2.imwrite(output_path +'/'+ str(name) + '.jpg',frame)
            cv2.waitKey(1)
            name = name + 1
        c = c + 1
    vc.release()

def process():
    # Current path
    source = get_env_value("SOURCE_PATH")
    output_folder = os.getcwd() + "/../video/output/"
    # take the new video and move it to a output folder
    for video in get_list_of_files(source):
        datetime_object = datetime.datetime.now()
        print("new video found: " + video + " at " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        video_folder = output_folder + str(datetime_object.month) + str(datetime_object.day) + str(datetime_object.hour) + str(datetime_object.minute) + str(datetime_object.second) + str(datetime_object.microsecond)
        os.mkdir(video_folder)
        frames_folder = video_folder + "/frames"
        os.mkdir(frames_folder)
        os.rename(video, video_folder + "/video.h264")
        # We have now /output/91520328263175/video.h264

        # Instantiate the video helper to extract the frames
        extract_frames(video_folder + "/video.h264", frames_folder, int(get_env_value("FRAMES_INTERVAL")))
        outcome = False
        for frame in get_list_of_files(frames_folder):
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
    # Analyse the new video
    outcome = process()
    # If the outcome is positive, send a notification
    if outcome:
        notify(outcome)
    time.sleep(4)

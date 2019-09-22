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

def prepare_video(video, output_folder):
    datetime_object = datetime.datetime.now()
    print("new video found: " + video + " at " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    video_folder = output_folder + str(datetime_object.month) + str(datetime_object.day) + str(datetime_object.hour) + str(datetime_object.minute) + str(datetime_object.second) + str(datetime_object.microsecond)
    os.mkdir(video_folder)
    
    frames_folder = video_folder + "/frames"
    os.mkdir(frames_folder)
    # Get the camera number, so we can apply custom masks to the frames
    camera = video.split('/')[-3]
        
    video_name = video.split('/')[-1]
    os.rename(video, video_folder + "/" + video_name)
    # We have now /output/91520328263175/video.h264 , let's extract the frames
    extract_frames(video_folder + "/" + video_name, frames_folder, int(get_env_value("FRAMES_INTERVAL")))
    
    # Get the list of frames, so we can order and analyse them
    frames = get_list_of_files(frames_folder)
    frames.sort(key=lambda f: os.path.getmtime(f))

    if camera == "02":
        resized_frames_folder = video_folder + "/resized_frames"
        os.mkdir(resized_frames_folder)
        for frame in frames:
            frame_name = frame.split('/')[-1]
            img = cv2.imread(frame)
            if img is not None:
                shape = img.shape
                height = img.shape[0]
                width = img.shape[1]
                crop_img = img[100:height, 0:width-400]
                # Save the cropped image
                cv2.imwrite(resized_frames_folder + '/' + frame_name, crop_img)
        frames = get_list_of_files(resized_frames_folder)
        frames.sort(key=lambda f: os.path.getmtime(f))

    return video_folder, frames

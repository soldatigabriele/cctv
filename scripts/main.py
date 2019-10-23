#!/usr/bin/env python3
import os
import json
import time
import shutil
from settings import * 
import os.path as path
from notification import *
from datetime import datetime
from model import analyse_image
from video import prepare_video
from modules.database import Database
from modules.json_helper import JsonHelper

def process():
    output_folder = os.getcwd() + "/../video/output/"
    # Take the new video and move it to the output folder
    for video in get_list_of_files(get_env_value("SOURCE_PATH")):
        # Create video Model
        database = Database()

        event_id = database.createEvent({
            'filename': path.basename(video),
            'timestamp': datetime.now()
        })

        video_folder, total_frames, frames = prepare_video(video, output_folder, event_id)

        attributes = {
            'video_folder': path.basename(video_folder),
            'total_frames': total_frames,
            'skipped_frames': get_env_value("FRAMES_INTERVAL"),
            'camera': video.split('/')[-3]
        }

        # Now that we have extracted the frames from the video, let's start the analysis 
        outcome = False
        frame_counter = 0
        for frame in frames:
            frame_counter = frame_counter + 1
            log("analysing: " + frame, "debug")
            outcome, attributes = analyse_image(frame, video_folder, attributes)
            if outcome:
                log("object found", "info")
                attributes['frame'] = frame_counter * int(get_env_value("FRAMES_INTERVAL"))
                break

        # If the outcome is not True, delete the folder with the video and frames
        if not outcome:
            log("No object found. Removing folder", "info")
            shutil.rmtree(video_folder, ignore_errors=True)

        # Serialize the labels
        try:
            attributes['labels_found'] = json.dumps(attributes['labels_found'], cls=JsonHelper)
        except expression:
            log('could not dump the attributes to array. Probably the attributes obj did not have the labels_found key', 'error')

        database.updateEvent(event_id, attributes)
        return outcome
    return None

def cleanup():
    current_time = time.time()
    for f in listdir_nohidden(os.getcwd() + "/../video/output"):
        folder_path = os.getcwd() + "/../video/output/" + f
        creation_time = os.path.getctime(folder_path)
        if (current_time - creation_time) // (24 * 3600) >= int(get_env_value('KEEP_RECORDS_FOR_DAYS')):
            shutil.rmtree(folder_path, ignore_errors=True)
            print('{} removed'.format(folder_path))

# Start the loop
while True:
    try:
        # Analyse the new video
        outcome = process()
        # If the outcome is positive, send a notification
        if outcome:
            notify(outcome)
        # Delete old files
        cleanup()
    except:
        log("Exception occurred", 'error')
        send_message("An error occurred at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        time.sleep(60)
    time.sleep(1)

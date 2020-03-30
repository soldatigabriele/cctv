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
    for video in get_list_of_files(config("General.SourcePath")):
        # Get the camera number from the video path
        camera_number = video.split('/')[-3]

        # Check if the camera is enabled, if not delete the video and return
        if not camera_config(camera_number, "Enabled", "bool"):
            log("Camera is not enabled", "info")
            os.unlink(video)
            return False, None

        # Create video Model
        database = Database()

        event_id = database.createEvent({
            'filename': path.basename(video),
            'timestamp': datetime.now()
        })

        # Prepare the frames for further analysis
        video_folder, total_frames, frames = prepare_video(
            video, output_folder, event_id)

        frames_interval = camera_config(camera_number, "FramesInterval")

        attributes = {
            'video_folder': path.basename(video_folder),
            'total_frames': total_frames,
            'skipped_frames': frames_interval,
            'camera': camera_number
        }

        # If we want to notify in any case, let's skip the object detection
        if camera_config(camera_number, "NotifyAlways"):
            database.updateEvent(event_id, attributes)
            return frames[1], camera_number

        # Now that we have extracted the frames from the video, let's start the analysis
        outcome = False
        frame_counter = 0
        for frame in frames:
            frame_counter = frame_counter + 1
            log("analysing: " + frame, "debug")
            outcome, attributes = analyse_image(
                camera_number, frame, video_folder, attributes)
            if outcome:
                log("object found", "info")
                attributes['frame'] = frame_counter * int(frames_interval)
                break

        # If the outcome is not True, delete the folder with the video and frames
        if not outcome:
            log("No object found", "info")
            if camera_config(camera_number, "DeleteVideosIfNothingFound", "bool"):
                log("Deleting {}".format(video_folder), "info")
                shutil.rmtree(video_folder, ignore_errors=True)

        # Serialize the labels
        try:
            attributes['labels_found'] = json.dumps(
                attributes['labels_found'], cls=JsonHelper)
        except:
            log('could not dump the attributes to array. Probably the attributes obj did not have the labels_found key', 'error')

        database.updateEvent(event_id, attributes)
        return outcome, camera_number
    return None, None


def cleanup():
    current_time = time.time()
    for f in listdir_nohidden(os.getcwd() + "/storage/logs"):
        folder_path = os.getcwd() + "/storage/logs/" + f
        creation_time = os.path.getctime(folder_path)
        if (current_time - creation_time) // (24 * 3600) >= int(config('General.KeepLogsForDays')):
            shutil.rmtree(folder_path, ignore_errors=True)
            log('{} deleted as older than threshold'.format(folder_path), "info")
    for f in listdir_nohidden(os.getcwd() + "/../video/output"):
        folder_path = os.getcwd() + "/../video/output/" + f
        creation_time = os.path.getctime(folder_path)
        if (current_time - creation_time) // (24 * 3600) >= int(config('General.KeepRecordsForDays')):
            shutil.rmtree(folder_path, ignore_errors=True)
            log('{} deleted as older than threshold'.format(folder_path), "info")
    # Delete the messages older than 47h from Telegram chats
    messages = database.getMessages()
    for message_id in messages:
        chat_id = messages[message_id]
        log("deleting message {} from chat {} as older than 47h".format(message_id, chat_id), "info")
        bot = telegram.Bot(token=config("Telegram.Token"))
        bot.delete_message(chat_id, message_id)
        # Delete the record from the database
        database.deleteMessage(message_id)


# Start the loop
while True:
    try:
        # Analyse the new video
        outcome, camera_number = process()
        # If the outcome is positive, send a notification for the camera channel
        if outcome:
            notify(camera_number, outcome)
        # Delete old files
        cleanup()
    except:
        log("Exception occurred", 'error')
        send_message( "01", "An error occurred at " +
                     datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        time.sleep(60)
    time.sleep(1)

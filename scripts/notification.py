import os
import cv2
import shutil
import imageio
import telegram
import datetime
from settings import *

def send_message(message="",):
    if get_env_value("NOTIFICATION_DRIVER") == 'telegram':
        bot = telegram.Bot(token=get_env_value("TELEGRAM_TOKEN"))
        try:
            bot.send_message(get_env_value("TELEGRAM_CHAT_ID"), message)
        except:
            log('error sending the telegram message at ' + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'error')
    else:
        log(message)

def send_photo(photo, caption=""):
    if get_env_value("NOTIFICATION_DRIVER") == 'telegram':
        bot = telegram.Bot(token=get_env_value("TELEGRAM_TOKEN"))
        caption = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if photo is not None: 
            bot.send_photo(get_env_value("TELEGRAM_CHAT_ID"), photo=open(photo, 'rb'), caption=caption)
    if get_env_value("NOTIFICATION_DRIVER") == 'python':
        cv2.imshow('image', cv2.imread(photo))
    else:
        log('object detected at: ' + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


def send_animation(photo, caption=""):
    if get_env_value("NOTIFICATION_DRIVER") == 'telegram':
        bot = telegram.Bot(token=get_env_value("TELEGRAM_TOKEN"))
        caption = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if photo is not None: 
            try:
                bot.send_animation(get_env_value("TELEGRAM_CHAT_ID"), animation=open(photo, 'rb'), caption=caption)
            except:
                msg = photo + "is too big to be sent"
                log(msg)
                send_message(msg)
    else:
        log('object detected at: ' + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def prepare_gif(photo):
    # Get the path to the video
    path = os.path.dirname(photo) + "/.."
    tmp_folder = path + "/tmp"
    os.mkdir(tmp_folder)

    # Compress the images
    i = 0
    files = get_list_of_files(path + "/frames")
    files.sort(key=lambda f: os.path.getmtime(f))
    for file in files:
        img = cv2.imread(file)
        resize_ratio = 0.5
        # Resize the image to make the process faster
        if img is not None: 
            img = cv2.resize(img, None, fx=resize_ratio, fy=resize_ratio)
            cv2.imwrite(tmp_folder + "/" + str(i) + ".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 10])
            i = i + 1

    # Create the GIF
    files = get_list_of_files(tmp_folder)
    files.sort(key=lambda f: os.path.getmtime(f))
    images= []
    for file in files:
        images.append(imageio.imread(file))


    # Remove tmp folder
    shutil.rmtree(tmp_folder, ignore_errors=True)

    gif = path + "/detection.gif"
    imageio.mimsave(gif, images)
    return gif

def notify(photo, caption=""):
    # Send the photo to telegram
    send_photo(photo, caption)

    if get_env_value("INCLUDE_GIF") in ["True", "true", "yes"]:
        gif = prepare_gif(photo)
        send_animation(gif, caption)
        

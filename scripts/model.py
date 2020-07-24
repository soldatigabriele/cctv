import os
import cv2
import sys
import json
import requests
from models.ssd import Ssd
from models.yolo import Yolo
from settings import * 
from dotenv import load_dotenv

def resolveModel(name):
    ''' Check if the driver is supported '''
    if name not in ["Yolo", "Ssd"]:
        raise Exception('Supported drivers for detection are Yolo and Ssd')
    return name

def get_predictions(camera_number, imagePath, threshold):

    # The driver should be Yolo or Ssd
    driver = camera_config(camera_number, "ModelDriver")
    model = resolveModel(driver)
    modelClass = getattr(sys.modules[__name__], model)()
    response = modelClass.analyse(imagePath, threshold)
    if response["status"] == "ok":
        # Predictions will be an empty array if nothing is found
        return response["predictions"]
    else:
        log(str(response), 'error')

# Draw the bounding box around the objects found
def draw_box(detection_box, label, img):
    height, width, channels = img.shape
    top= int(detection_box[0] * height)
    left= int(detection_box[1] * width)
    bottom= int(detection_box[2] * height)
    right= int(detection_box[3] * width)
    cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 1)
    cv2.putText(img,label,(left,top-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
    return

def analyse_image(camera_number, path, output_path, attributes):
    # Import the image
    img = cv2.imread(path)
    if img is None:
        return False, attributes

    resize_ratio = float(camera_config(camera_number, "ModelResizeRatio"))
    # Resize the image to make the process faster
    img = cv2.resize(img, None, fx=resize_ratio, fy=resize_ratio)

    # Get the predictions
    threshold = float(camera_config(camera_number, "ModelThreshold"))
    predictions = get_predictions(camera_number, path, threshold)

    # Check if the predictions contain person, if so return the path to the image
    match_found = False
    attributes['model'] = camera_config(camera_number, "ModelDriver")

    if 'labels_found' not in attributes.keys(): 
        attributes['labels_found'] = {}

    for prediction in predictions:

        # Store the label in the logs only if the probability is a minimum of 50%
        label = prediction['label']
        if(prediction['probability'] > 0.3):
            if label in attributes['labels_found']:
                wehave = attributes['labels_found'][prediction['label']]
                if wehave and wehave['probability'] < prediction['probability']:
                    # If we already have the key, update it if we have found something better
                    attributes['labels_found'][prediction['label']]['probability'] = float(prediction['probability'])
                    attributes['labels_found'][label]['detection_box'] = prediction['detection_box']
            else:
                # We don't have the key. Let's set them
                attributes['labels_found'][label] = {}
                attributes['labels_found'][label]['probability'] = float(prediction['probability'])
                attributes['labels_found'][label]['detection_box'] = prediction['detection_box']

        log(prediction['label'] + ": " + str(round(prediction['probability'], 4)*100) + "%")
        labels_list = camera_config(camera_number, "ModelLabels")
        if labels_list is None:
            labels_list = 'all'
        labels_list = labels_list.split(",")
        for label in labels_list:
            # Draw the bounding box around the objects
            if prediction['label'] == label or label == 'all':
                draw_box(prediction['detection_box'], prediction['label'] + " " + str(round(prediction['probability'], 4)*100) + "%", img)
                log(prediction['label'] + ": " + str(round(prediction['probability'], 4)*100) + "%", "info")
                if not os.path.exists(output_path + "/detected"):
                    os.mkdir(output_path + "/detected")
                # generate the new path name
                path = match_found = output_path + '/detected/' + os.path.basename(path)
                attributes['payload'] = json.dumps(str(predictions))
                attributes['confidence'] = float(round(prediction['probability'], 4))
                attributes['object_label'] = prediction['label']
                cv2.imwrite(path, img) 

    attributes['outcome'] = bool(match_found)
    return match_found, attributes

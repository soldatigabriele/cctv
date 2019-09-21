import os
import cv2
import json
import requests
from dotenv import load_dotenv
from settings import get_env_value 

def get_predictions(imagePath, threshold):
    url = get_env_value("MODEL_LOCATION") + '/model/predict?threshold=' + str(threshold)
    files = {'image': open(imagePath, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        # Predictions will be an empty array if nothing is found
        return json.loads(response.content)['predictions']
    else:
        print("error" + str(response))

# Draw the bounding box around the objects found
def draw_box(detection_box, label, img):
    # img = cv2.imread(path)
    height, width, channels = img.shape
    top= int(detection_box[0] * height)
    left= int(detection_box[1] * width)
    bottom= int(detection_box[2] * height)
    right= int(detection_box[3] * width)
    cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 1)
    cv2.putText(img,label,(left+5,top+10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
    return

def analyse_image(path, output_path):
    # Import the image
    img = cv2.imread(path)

    resize_ratio = float(get_env_value("MODEL_RESIZE_RATIO"))
    # Resize the image to make the process faster
    img = cv2.resize(img, None, fx=resize_ratio, fy=resize_ratio)

    # Get the predictions
    threshold = float(get_env_value("MODEL_THRESHOLD"))
    predictions = get_predictions(path, 0.1)

    # Check if the predictions contain person, if so send the notification
    match_found = False
    for prediction in predictions:
        print(prediction['label'] + ": " + str(round(prediction['probability'], 4)*100) + "%")
        labels_list = get_env_value("MODEL_LABELS")
        if labels_list is None:
            labels_list = 'all'
        labels_list = labels_list.split(",")
        for label in labels_list:
            # Draw the bounding box around the objects
            if prediction['label'] == label or label == 'all' and prediction['probability'] >= threshold:
                draw_box(prediction['detection_box'], prediction['label'] + " " + str(round(prediction['probability'], 4)*100) + "%", img)
                if not os.path.exists(output_path + "/detected"):
                    os.mkdir(output_path + "/detected")
                # generate the new path name
                path = match_found = output_path + '/detected/' + os.path.basename(path)
                cv2.imwrite(path, img) 

    return match_found
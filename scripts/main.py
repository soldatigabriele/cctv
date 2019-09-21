import os
import cv2
import sys
import json
import detection
from dotenv import load_dotenv

# Draw the bounding box around the objects found
def drawBox(detection_box, label, img):
    # img = cv2.imread(path)
    height, width, channels = img.shape
    top= int(detection_box[0] * height)
    left= int(detection_box[1] * width)
    bottom= int(detection_box[2] * height)
    right= int(detection_box[3] * width)
    cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 1)
    cv2.putText(img,label,(left+5,top+10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
    return

class Predictor:
    def detect(self, path, output_path):
        load_dotenv()
        # Import the image
        img = cv2.imread(path)

        resize_ratio = float(os.getenv("MODEL_RESIZE_RATIO"))
        # Resize the image to make the process faster
        img = cv2.resize(img, None, fx=resize_ratio, fy=resize_ratio)

        # Get the predictions
        model = detection.Model()
        threshold = float(os.getenv("MODEL_THRESHOLD"))
        predictions = model.detect(path, threshold)

        # Check if the predictions contain person, if so send the notification
        match_found = False
        for prediction in predictions:
            labels_list = os.getenv("MODEL_LABELS")
            if labels_list is None:
                labels_list = 'all'
            labels_list = labels_list.split(",")
            for label in labels_list:
                # Draw the bounding box around the objects
                if prediction['label'] == label or label == 'all':
                    drawBox(prediction['detection_box'], prediction['label'] + " " + str(round(prediction['probability'], 4)*100) + "%", img)
                    if not os.path.exists(output_path + "/detected"):
                        os.mkdir(output_path + "/detected")
                    # generate the new path name
                    path = match_found = output_path + '/detected/' + os.path.basename(path)
                    cv2.imwrite(path, img) 

        return match_found
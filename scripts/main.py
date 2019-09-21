import os
import cv2
import sys
import json
import detection

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
    def detect(self, path, base_path):
        # Import the image
        img = cv2.imread(path)

        # Resize the image to make the process faster
        img = cv2.resize(img, None, fx=0.5, fy=0.5)

        # Get the predictions
        model = detection.Model
        predictions = model.detect(model, path, 0.5)

        # Check if the predictions contain person, if so send the notification
        person_found = False
        for prediction in predictions:
            # Draw the bounding box around the objects
            if prediction['label'] == 'person' and prediction['probability'] >= 0.5 :
                drawBox(prediction['detection_box'], prediction['label'] + " " + str(round(prediction['probability'], 4)*100) + "%", img)
                if not os.path.exists(base_path + "/detected"):
                    os.mkdir(base_path + "/detected")
                # generate the new path name
                path = person_found = base_path + '/detected/' + os.path.basename(path)
                cv2.imwrite(path, img) 

        return person_found
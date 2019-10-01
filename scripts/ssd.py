# python deep_learning_object_detection.py 
# --image images/example_01.jpg 
# --prototxt MobileNetSSD_deploy.prototxt.txt 
# --model MobileNetSSD_deploy.caffemodel

import os
import cv2
import time
import argparse
import numpy as np
from settings import *

def ssd(image_path, max_threshold=0.3):
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False,
        help="path to input image")
    ap.add_argument("-c", "--confidence", type=float, default=0.2,
        help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    model_path = os.getcwd() + "/SSD/MobileNetSSD_deploy.caffemodel"
    prototxt_path = os.getcwd() + "/SSD/MobileNetSSD_deploy.prototxt.txt"
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    # (note: normalization is done via the authors of the MobileNet SSD
    # implementation)
    # image_path = os.getcwd() + "/../video/1.jpg"
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    # start = time.time()
    detections = net.forward()
    # end = time.time()

    # show timing information on YOLO
    # print("[INFO] SSD took {:.6f} seconds".format(end - start))


    output = {
        "status": "ok",
        "predictions": []
    }

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > max_threshold:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = box.astype("int")

            prediction = {
                "label_id": idx,
                "label": CLASSES[idx],
                "probability": confidence,
                "detection_box": [(startY/H), (startX/W), (endY/H), (endX/W)]
            }
            # append the prediction
            output["predictions"].append(prediction)

    return output


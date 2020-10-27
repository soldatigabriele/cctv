import os
import cv2
import time
import numpy as np
from settings import *


class Yolo(object):

    # The path to the weights and configuration. You will need a
    # folder models/yolo with "yolov3.weights" and "yolov3.cfg" inside.
    modelPath = "models/yolo"

    def analyse(self, image_path, max_threshold=0.5):
        # TODO I'm not sure what's the difference, I'll keep them the same for now
        max_confidence = max_threshold

        # load the COCO class labels our YOLO model was trained on
        labelsPath = os.path.sep.join([self.modelPath, "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
            dtype="uint8")

        # derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([self.modelPath, "yolov3.weights"])
        configPath = os.path.sep.join([self.modelPath, "yolov3.cfg"])

        # load our YOLO object detector trained on COCO dataset (80 classes)
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        # load our input image and grab its spatial dimensions
        # image = cv2.imread(args["image"])
        image = cv2.imread(image_path)
        (H, W) = image.shape[:2]

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        net.setInput(blob)
        # start = time.time()
        layerOutputs = net.forward(ln)
        # end = time.time()

        # show timing information on YOLO
        # print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > max_confidence:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, max_confidence, max_threshold)

        output = {
            "status": "ok",
            "predictions": []
        }

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                prediction = {
                    "label_id": classIDs[i],
                    "label": LABELS[classIDs[i]],
                    "probability": confidences[i],
                    "detection_box": [(y/H), (x/W), ((y+h)/H), ((x+w)/W)]
                }
                # append the prediction
                output["predictions"].append(prediction)

        return output
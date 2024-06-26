import cv2
import numpy as np

color_box = (0, 255, 0)  # Create a color_box color
thres = 0.45  # Threshold to detect objects
nms_threshold = 0.2  # Non-maximum suppression threshold

cap = cv2.VideoCapture(2)  # Load a video
cap.set(3, 640)  # Set the width
cap.set(4, 480)  # Set the height
cap.set(10, 100)  # Set the brightness

# Load the pre-trained model
class_name = [
    "Face",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "street sign",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "hat",
    "backpack",
    "umbrella",
    "shoe",
    "eye glasses",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "plate",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "mirror",
    "dining table",
    "window",
    "desk",
    "toilet",
    "door",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "blender",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
    "hair brush",
]  # Create an empty list to store the class names

config_path = (
    "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"  # Path to the configuration file
)
weights_path = "frozen_inference_graph.pb"  # Path to the pre-trained model

net = cv2.dnn_DetectionModel(weights_path, config_path)  # Load the model
net.setInputSize(320, 320)  # Set the input size
net.setInputScale(1.0 / 127.5)  # Set the input scale
net.setInputMean((127.5, 127.5, 127.5))  # Set the input mean
net.setInputSwapRB(True)  # Set the input swapRB

while True:  # Loop through the video
    success, img = cap.read()  # Read the video
    class_ids, confs, bbox = net.detect(
        img, confThreshold=thres
    )  # Detect objects in the image
    bbox = list(bbox)  # Convert the bounding box to a list
    confs = list(
        np.array(confs).reshape(1, -1)[0]
    )  # Convert the confidence to a list and reshape it
    confs = list(map(float, confs))  # Convert the confidence to a float

    # nmsthreshold=0.4, confThreshold=0.5 Setting the non-maximum suppression threshold and the confidence threshold
    # pagmasmababa ang confThreshold, mas maraming objects ang ma-detect
    indices = cv2.dnn.NMSBoxes(
        bbox, confs, thres, nms_threshold
    )  # Apply non-maximum suppression

    for i in indices:  # Loop through the indices
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(
            img, (x, y), (x + w, h + y), color=color_box, thickness=2
        )  # Draw a rectangle around the object
        cv2.putText(
            img,
            class_name[class_ids[i] - 1].upper(),
            (box[0] + 10, box[1] + 50),
            cv2.FONT_HERSHEY_COMPLEX,
            2,
            color_box,
            2,
        )  # Put the class name on the image

    cv2.imshow("Output", img)  # Display the image
    cv2.waitKey(1)  # Wait for a key press

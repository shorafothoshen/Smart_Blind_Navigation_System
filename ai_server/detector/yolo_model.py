from ultralytics import YOLO
import cv2
import numpy as np

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

def detect_objects(image_path):
    # read image
    img = cv2.imread(image_path)

    # run prediction
    results = model(img)

    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            name = model.names[cls_id]

            detections.append({
                "object": name,
                "confidence": round(conf, 2)
            })

    return detections
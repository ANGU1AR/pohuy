from ultralytics import YOLO
import cv2
import numpy as np
import torch
from torch import nn  # For Places365

# YOLO model
yolo_model = YOLO('yolov8n.pt')  # Fine-tune later

# Places365 model (from GitHub/CSAILVision/places365)
places_model = torch.hub.load('CSAILVision/places365', 'resnet50_places365')  # Pretrained
places_model.eval()

def detect_buildings(file_path: str) -> dict:
    img = cv2.imread(file_path)
    results = yolo_model(img)
    for result in results:
        boxes = result.boxes
        if boxes:
            box = boxes[0].xyxy.tolist()[0]
            return {"x1": box[0], "y1": box[1], "x2": box[2], "y2": box[3]}
    return {}

def detect_scene(file_path: str) -> list:
    img = Image.open(file_path).convert('RGB')
    input = places_model.preprocess(img)  # Assume preprocess from repo
    output = places_model(input)
    _, preds = torch.max(output, 1)
    return [places_model.categories[pred] for pred in preds]  # e.g., ['urban', 'building']
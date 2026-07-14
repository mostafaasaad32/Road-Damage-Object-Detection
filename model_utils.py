import os
import streamlit as st
from ultralytics import YOLO
from huggingface_hub import hf_hub_download
import cv2
import numpy as np
from PIL import Image

# Class definitions and visual styling tokens
CLASS_NAMES = {
    0: 'Longitudinal Crack',
    1: 'Transverse Crack',
    2: 'Alligator Crack',
    3: 'Other Corruption',
    4: 'Pothole'
}

# Hex colors for UI & badges
CLASS_COLORS_HEX = {
    0: '#06B6D4',  # Electric Cyan
    1: '#F97316',  # Neon Orange
    2: '#EC4899',  # Magenta Pink
    3: '#EAB308',  # Bright Yellow
    4: '#10B981'   # Emerald Green
}

# RGB colors for PIL/OpenCV drawing
CLASS_COLORS_RGB = {
    0: (6, 182, 212),
    1: (249, 115, 22),
    2: (236, 72, 153),
    3: (234, 179, 8),
    4: (16, 185, 129)
}

def fetch_model_from_hub():
    """
    Downloads and retrieves pre-trained YOLOv8m model weights directly from the Hugging Face Hub.
    Does not load or check for local model files.
    """
    st.info("🌐 Fetching pre-trained YOLOv8m model weights directly from Hugging Face Hub (`mostafaasaad32/yolo_road_crack_detection`)...")
    downloaded_path = hf_hub_download(
        repo_id="mostafaasaad32/yolo_road_crack_detection",
        filename="best_overall_model.pt"
    )
    return downloaded_path

@st.cache_resource(show_spinner=False)
def load_best_model():
    """
    Loads and caches our best-performing model (YOLOv8m / best_overall_model) directly from Hugging Face Hub for instant inference.
    """
    pt_path = fetch_model_from_hub()
    model = YOLO(pt_path)
    return model, pt_path

def draw_custom_boxes(image_pil, results, conf_threshold=0.25):
    """
    Draws vibrant, high-contrast bounding boxes with custom class colors and badges on PIL Image.
    Returns annotated PIL Image and list of detected objects summary.
    """
    img_np = np.array(image_pil.convert("RGB"))
    detections_summary = []
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = float(box.conf[0])
            if conf < conf_threshold:
                continue
                
            cls_id = int(box.cls[0])
            cls_name = CLASS_NAMES.get(cls_id, f"Class {cls_id}")
            rgb = CLASS_COLORS_RGB.get(cls_id, (255, 255, 255))
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Draw glowing double bounding box for premium look
            cv2.rectangle(img_np, (x1, y1), (x2, y2), rgb, 3)
            
            # Prepare label
            label = f"{cls_name} ({conf*100:.1f}%)"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            (label_w, label_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            
            # Draw filled header box for text
            cv2.rectangle(img_np, (x1, max(0, y1 - label_h - 10)), (x1 + label_w + 10, y1), rgb, -1)
            
            # Draw text in white or dark depending on brightness
            brightness = (rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114)
            text_color = (0, 0, 0) if brightness > 150 else (255, 255, 255)
            cv2.putText(img_np, label, (x1 + 5, max(15, y1 - 5)), font, font_scale, text_color, thickness)
            
            detections_summary.append({
                "Class ID": cls_id,
                "Damage Type": cls_name,
                "Confidence": round(conf * 100, 2),
                "Bounding Box": f"[{x1}, {y1}, {x2}, {y2}]",
                "Color Hex": CLASS_COLORS_HEX.get(cls_id, "#FFFFFF")
            })
            
    return Image.fromarray(img_np), detections_summary

def calculate_severity_score(detections_summary):
    """
    Calculates an estimated road maintenance priority & severity index (0 - 100) based on damage types.
    Potholes & Alligator Cracks carry higher structural weight.
    """
    if not detections_summary:
        return 0.0, "Excellent (No Visible Damage)", "#10B981"
        
    weights = {
        'Pothole': 35.0,
        'Alligator Crack': 28.0,
        'Transverse Crack': 18.0,
        'Longitudinal Crack': 15.0,
        'Other Corruption': 10.0
    }
    
    total_score = 0.0
    for d in detections_summary:
        dmg = d["Damage Type"]
        conf = d["Confidence"] / 100.0
        total_score += weights.get(dmg, 10.0) * conf
        
    final_score = min(100.0, total_score)
    
    if final_score >= 65.0:
        return round(final_score, 1), "Critical - Immediate Maintenance Required", "#EF4444"
    elif final_score >= 35.0:
        return round(final_score, 1), "Moderate - Scheduled Repair Recommended", "#F97316"
    else:
        return round(final_score, 1), "Minor - Routine Monitoring", "#EAB308"

import cv2
import os
from utils.file_handling import get_output_path
from django.conf import settings

def detect_faces(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
        
    # Load Haar cascade
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        # Draw bounding box around faces
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 183, 178), 3) # Pastel pink box
        
    out_path, out_url = get_output_path(image_path, "detected")
    cv2.imwrite(out_path, img)
    
    return out_url

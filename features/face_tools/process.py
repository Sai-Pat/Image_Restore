import cv2
import os
from utils.file_handling import get_output_path
from django.conf import settings

def blur_faces(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
        
    # Load Haar cascade
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        # Extract the region of the image that contains the face
        face_roi = img[y:y+h, x:x+w]
        # Apply gaussian blur
        blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
        # Put the blurred face back into the image
        img[y:y+h, x:x+w] = blurred_face
        
    out_path, out_url = get_output_path(image_path, "blurred")
    cv2.imwrite(out_path, img)
    
    return out_url

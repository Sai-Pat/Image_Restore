import cv2
import os
from utils.file_handling import get_output_path

def draw_magic_eyes(frame, eyes):
    for (ex, ey, ew, eh) in eyes:
        center = (ex + ew//2, ey + eh//2)
        radius = int(round((ew + eh)*0.25))
        cv2.circle(frame, center, radius, (255, 183, 178), 3) # Pastel pink
        cv2.circle(frame, center, radius+5, (199, 206, 234), 1) # Pastel purple glow
    return frame

def process_eye_tracking(file_path):
    # Determine if it's a video or image
    ext = file_path.split('.')[-1].lower()
    is_video = ext in ['mp4', 'avi', 'mov', 'mkv']
    
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    if is_video:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file.")
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps == 0: fps = 30
        
        out_path, out_url = get_output_path(file_path, "tracked_video")
        # Ensure it saves as mp4 for web compatibility
        out_path = out_path.rsplit('.', 1)[0] + '.mp4'
        out_url = out_url.rsplit('.', 1)[0] + '.mp4'
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1') # Better web compatibility
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
        
        max_frames = 300 # Limit to 10 seconds at 30fps to avoid timeouts
        frame_count = 0
        
        while cap.isOpened() and frame_count < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
            frame = draw_magic_eyes(frame, eyes)
            out.write(frame)
            frame_count += 1
            
        cap.release()
        out.release()
        return out_url, True # is_video
    else:
        img = cv2.imread(file_path)
        if img is None:
            raise ValueError("Could not read image file.")
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        img = draw_magic_eyes(img, eyes)
        
        out_path, out_url = get_output_path(file_path, "tracked")
        cv2.imwrite(out_path, img)
        return out_url, False # not video

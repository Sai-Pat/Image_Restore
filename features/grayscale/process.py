import cv2
from utils.file_handling import get_output_path

def convert_to_grayscale(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    out_path, out_url = get_output_path(image_path, "gray")
    cv2.imwrite(out_path, gray)
    
    return out_url

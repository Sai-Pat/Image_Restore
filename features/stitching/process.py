import cv2
import uuid
import os
from django.conf import settings

def stitch_images(image_paths):
    images = []
    for path in image_paths:
        img = cv2.imread(path)
        if img is not None:
            images.append(img)
            
    if len(images) < 2:
        raise ValueError("Need at least 2 images to stitch")
        
    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(images)
    
    if status != cv2.Stitcher_OK:
        raise Exception(f"Image stitching failed with status code {status}")
        
    filename = f"stitched_{uuid.uuid4()}.jpg"
    out_path = os.path.join(settings.MEDIA_ROOT, filename)
    cv2.imwrite(out_path, stitched)
    
    return f"{settings.MEDIA_URL}{filename}"

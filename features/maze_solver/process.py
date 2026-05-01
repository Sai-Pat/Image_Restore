import cv2
import numpy as np
from collections import deque
from utils.file_handling import get_output_path

def solve_maze(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Thresholding
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # Morphology to clean up noise
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # In thresh: walls are 255, path is 0
    # Let's invert so path is 255
    path_img = cv2.bitwise_not(thresh)
    
    h, w = path_img.shape
    
    # Find start (top row)
    start_point = None
    for x in range(w):
        if path_img[0, x] == 255:
            start_point = (x, 0)
            break
            
    # Find end (bottom row)
    end_point = None
    for x in range(w):
        if path_img[h-1, x] == 255:
            end_point = (x, h-1)
            break
            
    if not start_point or not end_point:
        # Fallback if no clear openings: top-left to bottom-right
        start_point = (1, 1)
        end_point = (w-2, h-2)
        
    # BFS
    queue = deque([start_point])
    visited = np.zeros_like(path_img, dtype=bool)
    visited[start_point[1], start_point[0]] = True
    parent = {}
    
    found = False
    
    # Directions: right, left, down, up
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while queue:
        curr = queue.popleft()
        
        if curr == end_point:
            found = True
            break
            
        for dx, dy in directions:
            nx, ny = curr[0] + dx, curr[1] + dy
            
            if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                if path_img[ny, nx] == 255: # Valid path
                    visited[ny, nx] = True
                    parent[(nx, ny)] = curr
                    queue.append((nx, ny))
                    
    if found:
        # Draw path on original image (pastel pink glowing color: BGR)
        curr = end_point
        path_color = (255, 183, 178) # Pastel pink
        thickness = max(1, w // 200) # Dynamic thickness
        
        while curr != start_point:
            prev = parent[curr]
            cv2.line(img, curr, prev, path_color, thickness)
            curr = prev
            
    out_path, out_url = get_output_path(image_path, "solved")
    cv2.imwrite(out_path, img)
    
    return out_url

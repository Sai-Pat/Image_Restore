import cv2
import numpy as np
from utils.file_handling import get_output_path

def compute_energy(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    energy = np.abs(sobel_x) + np.abs(sobel_y)
    return energy

def find_seam(energy):
    r, c = energy.shape
    M = energy.copy()
    backtrack = np.zeros_like(M, dtype=int)
    
    for i in range(1, r):
        for j in range(c):
            if j == 0:
                idx = np.argmin(M[i-1, j:j+2])
                backtrack[i, j] = idx + j
                min_energy = M[i-1, idx + j]
            else:
                idx = np.argmin(M[i-1, j-1:j+2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i-1, idx + j - 1]
            M[i, j] += min_energy

    seam = []
    j = np.argmin(M[-1])
    for i in range(r-1, -1, -1):
        seam.append((i, j))
        j = backtrack[i, j]
        
    return seam[::-1]

def remove_seam(img, seam):
    r, c, _ = img.shape
    output = np.zeros((r, c - 1, 3), dtype=np.uint8)
    for i, j in seam:
        output[i, :, 0] = np.delete(img[i, :, 0], j)
        output[i, :, 1] = np.delete(img[i, :, 1], j)
        output[i, :, 2] = np.delete(img[i, :, 2], j)
    return output

def carve_seams(image_path, num_seams=50):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")
        
    # Resize if too large to prevent extremely slow processing
    max_dim = 600
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
        
    out_img = img.copy()
    for _ in range(num_seams):
        energy = compute_energy(out_img)
        seam = find_seam(energy)
        out_img = remove_seam(out_img, seam)
        
    out_path, out_url = get_output_path(image_path, "carved")
    cv2.imwrite(out_path, out_img)
    
    return out_url

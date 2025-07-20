
import cv2
import numpy as np 

# Step 1: Buat matrix
matrix = np.array([
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
], dtype=np.uint8)

# Step 2: Distance transform pada area bebas (0)
dist = cv2.distanceTransform(1 - matrix, cv2.DIST_L2, 5)

print(dist)

# Step 3: Buat buffer di sekitar obstacle dengan radius tertentu
buffer_radius = 3
buffered_obstacle = np.uint8(dist < 2)

print(buffered_obstacle)

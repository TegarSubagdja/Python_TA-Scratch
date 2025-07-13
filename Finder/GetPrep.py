from Utils import *
import cv2
import numpy as np
import time

def Prep(img, start, goal, markSize):

    frame = img.copy()

    # Step 0: Grayscale jika RGB
    if len(frame.shape) == 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 1: Hapus marker robot (dengan lingkaran putih)
    if start is not None and goal is not None:
        pts1 = goal[0]
        pts2 = start[0]
        cv2.circle(frame, pts1, int(markSize), 255, -1)
        cv2.circle(frame, pts2, int(markSize), 255, -1)

    # Step 2: Threshold -> biner (rintangan = putih = 255)
    _, binary = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('Map_biner.jpg', binary)

    # Step 3: Erosi ringan untuk bersihkan noise
    kernel = np.ones((16, 16), np.uint8)
    clean = cv2.erode(binary, kernel, iterations=1)

    # Step 4: Distance Transform → buffer ke luar
    start_time = time.time()
    dist = cv2.distanceTransform(255 - clean, cv2.DIST_L2, 5)

    buffer_radius = int(markSize)  # pixel radius robot (½ diameter)
    buffered_obstacle = np.uint8(dist < buffer_radius) * 255
    end_time = time.time()
    print("Buffering time (distanceTransform):", end_time - start_time)

    # Step 5: Overlay visualisasi (buffer merah)
    if len(frame.shape) == 2:
        img_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    else:
        img_bgr = frame.copy()

    overlay = img_bgr.copy()
    overlay[buffered_obstacle == 255] = [0, 0, 255]  # merah di area buffer
    visual = cv2.addWeighted(img_bgr, 1, overlay, 0.5, 0)

    # Simpan hasil
    cv2.imwrite('Map_GetPath.jpg', buffered_obstacle)
    cv2.imwrite('Map_With_Buffer_Overlay.jpg', visual)

    # Kembalikan matrix peta
    return buffered_obstacle

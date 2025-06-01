import cv2
import numpy as np

def preprocessing(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 106, 255, cv2.THRESH_BINARY)

    kernel = np.ones((7, 7), np.uint8)
    closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    return opening

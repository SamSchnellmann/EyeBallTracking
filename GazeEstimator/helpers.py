import cv2
import mediapipe as mp
import numpy as np


relative = lambda landmark, shape: (int(landmark.x * shape[1]), int(landmark.y * shape[0]))
relativeT = lambda landmark, shape: (int(landmark.x * shape[1]), int(landmark.y * shape[0]), 0)

def calculate_focal_length(image, interocular_distance_mm):

    # Calculate focal length here
    print("Wow so cool... nothing yet")

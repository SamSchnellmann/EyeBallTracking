import cv2
import mediapipe as mp
import numpy as np


relative = lambda landmark, shape: (int(landmark.x * shape[1]), int(landmark.y * shape[0]))
relativeT = lambda landmark, shape: (int(landmark.x * shape[1]), int(landmark.y * shape[0]), 0)

def calculate_focal_length(image, interocular_distance_mm):
    # Calculate focal length here
    print("Wow so cool... nothing yet")

def move_mouse_joystick(current_position, point1, point2):

    divisor = 3
  
    nextx = current_position[0]
    nexty = current_position[1]

    diff_x = point2[0] - point1[0]
    diff_y = point2[1] - point1[1]

    if(diff_x < 0): # looking to the right
        nextx += int(diff_x / divisor)
    elif(diff_x > 0): # looking to the left
        nextx += int(diff_x / divisor)

    if(diff_y < 0): # Looking down 
        nexty += int(diff_y / divisor)
    elif(diff_y > 0): # looking up
        nexty += int(diff_y / divisor)
    

    return nextx, nexty

def move_mouse(point1, point2):

    nextx = 0
    nexty = 0

    max_left = 900
    max_right = 400

    if(point2[0] <= max_right):
        point2[0] == 0
    elif(point2[0] > max_left):
        point2[0] ==  500
    else:
        point2[0] -= 400


    


    return nextx, nexty

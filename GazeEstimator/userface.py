from helpers import relative, relativeT
import numpy as np


def calibrate(frame, points):
  
    # Finding where the landmarks are on screen relative to the center nose landmark
    chin_x = (((relativeT(points.landmark[4], frame.shape)[0]) - (relativeT(points.landmark[152], frame.shape)[0])))
    chin_y = (((relativeT(points.landmark[4], frame.shape)[1]) - (relativeT(points.landmark[152], frame.shape)[1])))
    lefteye_x = (((relativeT(points.landmark[4], frame.shape)[0]) - relativeT(points.landmark[263], frame.shape)[0]))
    lefteye_y = (((relativeT(points.landmark[4], frame.shape)[1]) - relativeT(points.landmark[263], frame.shape)[1]))
    righteye_x = (((relativeT(points.landmark[4], frame.shape)[0]) - relativeT(points.landmark[33], frame.shape)[0]))
    righteye_y = (((relativeT(points.landmark[4], frame.shape)[1]) - relativeT(points.landmark[33], frame.shape)[1]))
    leftmouth_x = (((relativeT(points.landmark[4], frame.shape)[0]) - relativeT(points.landmark[287], frame.shape)[0]))
    leftmouth_y = (((relativeT(points.landmark[4], frame.shape)[1]) - relativeT(points.landmark[287], frame.shape)[1]))
    rightmouth_x = (((relativeT(points.landmark[4], frame.shape)[0]) - relativeT(points.landmark[57], frame.shape)[0]))
    rightmouth_y = (((relativeT(points.landmark[4], frame.shape)[1]) - relativeT(points.landmark[57], frame.shape)[1]))


    # Adding new points to model array
    # Can be improved by accounting for z axis calibration as well
    model_points = np.array([
        (0.0, 0.0, 0.0),  # Nose tip
        (chin_x, chin_y, -12.5),  # Chin
        (lefteye_x, lefteye_y, -26),  # Left eye, left corner
        (righteye_x, righteye_y, -26),  # Right eye, right corner
        (leftmouth_x, leftmouth_y, -24.1),  # Left Mouth corner
        (rightmouth_x, rightmouth_y, -24.1)  # Right mouth corner
    ])

    TL_x = ((relative(points.landmark[4], frame.shape)[0]) - relative(points.landmark[105], frame.shape)[0])
    TL_y = ((relative(points.landmark[4], frame.shape)[1]) - relative(points.landmark[105], frame.shape)[1])

    TR_x = ((relative(points.landmark[4], frame.shape)[0]) - relative(points.landmark[334], frame.shape)[0])
    TR_y = ((relative(points.landmark[4], frame.shape)[1]) - relative(points.landmark[334], frame.shape)[1])

    BL_x = ((relative(points.landmark[4], frame.shape)[0]) - relative(points.landmark[172], frame.shape)[0])
    BL_y = ((relative(points.landmark[4], frame.shape)[1]) - relative(points.landmark[172], frame.shape)[1])

    BR_x = ((relative(points.landmark[4], frame.shape)[0]) - relative(points.landmark[397], frame.shape)[0])
    BR_y = ((relative(points.landmark[4], frame.shape)[1]) - relative(points.landmark[397], frame.shape)[1])

    C_x = ((relative(points.landmark[4], frame.shape)[0]) - relative(points.landmark[152], frame.shape)[0])
    C_y = ((relative(points.landmark[4], frame.shape)[1]) - relative(points.landmark[152], frame.shape)[1])


    Face_top_left = np.array([[TL_x], [TL_y], [-38]])
    Face_top_right = np.array([[TR_x], [TR_y], [-38]])
    Face_bottom_left = np.array([[BL_x], [BL_y], [-60]])
    Face_bottom_right = np.array([[BR_x], [BR_y], [-60]])
    Chin = np.array([[C_x], [C_y], [-12.5]])

    return model_points, Face_top_left, Face_top_right, Face_bottom_left, Face_bottom_right, Chin
import cv2
import numpy as np
from helpers import relative, relativeT
import helpers
import pyautogui
import userface
# import focallength


pyautogui.PAUSE = 0



flag = None
on_new_model = False

mouse_flag = None



def gaze(frame, points):

    #Global declaration of variables 
    global on_new_model, model_points, Top_left_mod, Top_right_mod, Bottom_left_mod, Bottom_right_mod, Chin_mod

    # Check flag and 'on_new_model' boolean before calibrating 'model_points' to user's face
    if flag is not None:

        if on_new_model is False:

            model_points, Top_left_mod, Top_right_mod, Bottom_left_mod, Bottom_right_mod, Chin_mod = userface.calibrate(frame, points)

            on_new_model = True

        else:
            cv2.putText(frame, "Calibrated", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        
    else:
        cv2.putText(frame, "Not Calibrated", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        on_new_model = False

        # Static 3d model points that are un-calibrated
        model_points = np.array([
            (0.0, 0.0, 0.0),  # Nose tip
            (0, -63.6, -12.5),  # Chin
            (-43.3, 32.7, -26),  # Left eye, left corner
            (43.3, 32.7, -26),  # Right eye, right corner
            (-28.9, -28.9, -24.1),  # Left Mouth corner
            (28.9, -28.9, -24.1)  # Right mouth corner
        ])

        Eye_ball_center_right = np.array([[-29.05], [32.7], [-39.5]])
        Eye_ball_center_left = np.array([[29.05], [32.7], [-39.5]])  # the center of the left eyeball as a vector.


    """
    The gaze function gets an image and face landmarks from mediapipe framework.
    The function draws the gaze direction into the frame.
    """

    '''
    2D image points.
    relative takes mediapipe points that are normalized to [-1, 1] and returns image points
    at (x,y) format
    '''
    image_points = np.array([
        relative(points.landmark[4], frame.shape),  # Nose tip
        relative(points.landmark[152], frame.shape),  # Chin
        relative(points.landmark[263], frame.shape),  # Left eye left corner
        relative(points.landmark[33], frame.shape),  # Right eye right corner
        relative(points.landmark[287], frame.shape),  # Left Mouth corner
        relative(points.landmark[57], frame.shape)  # Right mouth corner
    ], dtype="double")

    '''
    2D image points.
    relativeT takes mediapipe points that is normalized to [-1, 1] and returns image points
    at (x,y,0) format
    '''
    image_points1 = np.array([
        relativeT(points.landmark[4], frame.shape),  # Nose tip
        relativeT(points.landmark[152], frame.shape),  # Chin
        relativeT(points.landmark[263], frame.shape),  # Left eye, left corner
        relativeT(points.landmark[33], frame.shape),  # Right eye, right corner
        relativeT(points.landmark[287], frame.shape),  # Left Mouth corner
        relativeT(points.landmark[57], frame.shape)  # Right mouth corner
    ], dtype="double")



    # camera matrix estimation
    # This section regarding the camera will need to be ironed out for more accurate estimation
    # This will be what I (Arron) will work on next
    
    focal_length = frame.shape[1] 
    
    center = (frame.shape[1] / 2, frame.shape[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]], dtype="double"
    )


    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

     
    # Switch from just pupils to calibrated vectors if flag is up
    if flag is not None:
        face_top_left = relative(points.landmark[105], frame.shape)
        face_top_right = relative(points.landmark[334], frame.shape)
        face_chin = relative(points.landmark[152], frame.shape)

    else:
        # 2d pupil location
        left_pupil = relative(points.landmark[468], frame.shape)
        right_pupil = relative(points.landmark[473], frame.shape)

    # Transformation between static model points and user face
    _, transformation, _ = cv2.estimateAffine3D(image_points1, model_points)  # image to world transformation

    if transformation is not None:  # if estimateAffine3D is successful
        # project pupil image point into 3d world point 

        if flag is not None:

            # Making a t
            ftl_world_cord = transformation @ np.array([[face_top_left[0], face_top_left[1], 0, 1]]).T
            ftr_world_cord = transformation @ np.array([[face_top_right[0], face_top_right[1], 0, 1]]).T
            chin_world_cord = transformation @ np.array([[face_chin[0], face_chin[1], 0, 1]]).T

            # 3D gaze point estimated using the world Cordinates and Face vectors
            TL = Top_left_mod + (ftl_world_cord - Top_left_mod) * 20
            TR = Top_right_mod + (ftr_world_cord - Top_right_mod) * 20
            C = Chin_mod + (chin_world_cord - Chin_mod) * 20

            
            # Project the 3d vectors into the 2D plane
            (topLeft_2D, _) = cv2.projectPoints((int(TL[0]), int(TL[1]), int(TL[2])), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)
            
            (topRight_2D, _) = cv2.projectPoints((int(TR[0]), int(TR[1]), int(TR[2])), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)

            (chin_2D, _) = cv2.projectPoints((int(C[0]), int(C[1]), int(C[2])), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)


            # Project a 3d head pose into the image plane for each vector
            (TL_head_pose, _) = cv2.projectPoints((int(ftl_world_cord[0]), int(ftl_world_cord[1]), int(40)),
                                            rotation_vector,
                                            translation_vector, camera_matrix, dist_coeffs)
            
            (TR_head_pose, _) = cv2.projectPoints((int(ftr_world_cord[0]), int(ftr_world_cord[1]), int(40)),
                                            rotation_vector,
                                            translation_vector, camera_matrix, dist_coeffs)
            
            (Chin_head_pose, _) = cv2.projectPoints((int(chin_world_cord[0]), int(chin_world_cord[1]), int(40)),
                                            rotation_vector,
                                            translation_vector, camera_matrix, dist_coeffs)
            
            TL_vector = face_top_left + (topLeft_2D[0][0] - face_top_left) - (TL_head_pose[0][0] - face_top_left)
            TR_vector = face_top_right + (topRight_2D[0][0] - face_top_right) - (TR_head_pose[0][0] - face_top_right)
            Chin_vector = face_chin + (chin_2D[0][0] - face_chin) - (Chin_head_pose[0][0] - face_chin)


            """
            Chin vector was moving in opposite direction of the other two
            so this is reversing it to be in line with them
            """
            Chin_vector[0] = face_chin[0] + (face_chin[0] - Chin_vector[0])
            Chin_vector[1] = face_chin[1] + (face_chin[1] - Chin_vector[1])

            
            # Making start and end points of all three vectors
            startTL = (int(face_top_left[0]), int(face_top_left[1]))
            endTL = (int(TL_vector[0]), int(TL_vector[1]))
            startTR = (int(face_top_right[0]), int(face_top_right[1]))
            endTR = (int(TR_vector[0]), int(TR_vector[1]))
            startChin = (int(face_chin[0]), int(face_chin[1]))
            endChin = (int(Chin_vector[0]), int(Chin_vector[1]))


            # Creating average of the three vectors 
            start_avg_x = int((startTL[0] + startTR[0] + startChin[0]) / 3)
            start_avg_y = int((startTL[1] + startTR[1] + startChin[1]) / 3)
            end_avg_x = int((endTL[0] + endTR[0] + endChin[0]) / 3)
            end_avg_y = int((endTL[1] + endTR[1] + endChin[1]) / 3)

            startAvg = (start_avg_x, start_avg_y)
            endAvg = (end_avg_x, end_avg_y)


            # Drawing lines with generated vectors
            cv2.line(frame, startTL, endTL, (0, 0, 255), 2)
            cv2.line(frame, startTR, endTR, (0, 0, 255), 2)
            cv2.line(frame, startChin, endChin, (0, 0, 255), 2)
            cv2.line(frame, startAvg, endAvg,(0, 0, 255), 2)

            

            pyautogui.FAILSAFE = False
            nextpos = helpers.move_mouse_joystick(pyautogui.position(), startAvg, endAvg)
            pyautogui.moveTo(nextpos[0], nextpos[1])




        else:
            left_pupil_world_cord = transformation @ np.array([[left_pupil[0], left_pupil[1], 0, 1]]).T
            right_pupil_world_cord = transformation @ np.array([[right_pupil[0], right_pupil[1], 0, 1]]).T

            # 3D gaze point (10 is arbitrary value denoting gaze distance)
            LS = Eye_ball_center_left + (left_pupil_world_cord - Eye_ball_center_left) * 10
            RS = Eye_ball_center_right + (right_pupil_world_cord - Eye_ball_center_right) * 10

            # TL = 

            # Project a 3D gaze direction onto the image plane.
            (left_eye_pupil2D, _) = cv2.projectPoints((int(LS[0]), int(LS[1]), int(LS[2])), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)
            
            (right_eye_pupil2D, _) = cv2.projectPoints((int(RS[0]), int(RS[1]), int(RS[2])), rotation_vector,
                                                translation_vector, camera_matrix, dist_coeffs)
            
            
            # project 3D head pose into the image plane
            (L_head_pose, _) = cv2.projectPoints((int(left_pupil_world_cord[0]), int(left_pupil_world_cord[1]), int(40)),
                                            rotation_vector,
                                            translation_vector, camera_matrix, dist_coeffs)
            (R_head_pose, _) = cv2.projectPoints((int(right_pupil_world_cord[0]), int(right_pupil_world_cord[1]), int(40)),
                                            rotation_vector,
                                            translation_vector, camera_matrix, dist_coeffs)
            
            # correct gaze for head rotation
            gaze = left_pupil + (left_eye_pupil2D[0][0] - left_pupil) - (L_head_pose[0][0] - left_pupil)
            Rgaze = right_pupil + (right_eye_pupil2D[0][0] - right_pupil) - (R_head_pose[0][0] - right_pupil)


            # Draw gaze line into screen
            p1 = (int(left_pupil[0]), int(left_pupil[1]))
            p2 = (int(gaze[0]), int(gaze[1]))
            Rp1 = (int(right_pupil[0]), int(right_pupil[1]))
            Rp2 = (int(Rgaze[0]), int(Rgaze[1]))
            cv2.line(frame, p1, p2, (0, 0, 255), 2)
            cv2.line(frame, Rp1, Rp2, (0, 0, 255), 2)

    else:
        print("Transformation not found")
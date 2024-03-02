# Credit https://github.com/matthullstrung/gaze-estimation
# I cleaned up the code, and incorporated pyautogui


import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from collections import deque

############## PARAMETERS #######################################################

# Set these values to show/hide certain vectors of the estimation
draw_gaze = True
draw_full_axis = True
draw_headpose = False

# Gaze Score multiplier (Higher multiplier = Gaze affects headpose estimation more)
x_score_multiplier = 4
y_score_multiplier = 4

# Threshold of how close scores should be to average between frames
threshold = .3

#################################################################################

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                  refine_landmarks=True,
                                  max_num_faces=2,
                                  min_detection_confidence=0.6)
cap = cv2.VideoCapture(0)

face_3d = np.array([
    [0.0, 0.0, 0.0],  # Nose tip
    [0.0, -330.0, -65.0],  # Chin
    [-225.0, 170.0, -135.0],  # Left eye left corner
    [225.0, 170.0, -135.0],  # Right eye right corner
    [-150.0, -150.0, -125.0],  # Left Mouth corner
    [150.0, -150.0, -125.0]  # Right mouth corner
], dtype=np.float64)

# Reposition left eye corner to be the origin
leye_3d = np.array(face_3d)
leye_3d[:, 0] += 225
leye_3d[:, 1] -= 175
leye_3d[:, 2] += 135

# Reposition right eye corner to be the origin
reye_3d = np.array(face_3d)
reye_3d[:, 0] -= 225
reye_3d[:, 1] -= 175
reye_3d[:, 2] += 135

# Gaze scores from the previous frame
last_lx, last_rx = 0, 0
last_ly, last_ry = 0, 0

# Initialize deques for smoothing with a fixed window size
window_size = 5  # Adjustable based on desired smoothing effect
gaze_points_x = deque(maxlen=window_size)
gaze_points_y = deque(maxlen=window_size)


def prepare_image_for_face_mesh(cap):
    success, img = cap.read()
    if not success:
        return None  # or handle the failure to read from the capture

    # Flip + convert img from BGR to RGB
    img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    img.flags.writeable = False

    return success, img


def process_image_with_face_mesh(img, face_mesh):
    # Get the result
    results = face_mesh.process(img)

    # Make the image writeable again
    img.flags.writeable = True

    # Convert the color space from RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    face_2d = []  # Initialize or update the face landmarks here based on results

    return img, face_2d, results


def convert_landmarks_to_pixel_coordinates(face_landmarks, img_w, img_h):
    face_2d = []  # Initialize an empty list to hold the 2D coordinates

    for idx, lm in enumerate(face_landmarks.landmark):
        # Convert landmark x and y to pixel coordinates
        x, y = int(lm.x * img_w), int(lm.y * img_h)

        # Add the 2D coordinates to the array
        face_2d.append((x, y))

    return face_2d


def calculate_left_x_gaze_score(face_2d, last_lx, threshold):
    if (face_2d[243, 0] - face_2d[130, 0]) != 0:
        lx_score = (face_2d[468, 0] - face_2d[130, 0]) / (face_2d[243, 0] - face_2d[130, 0])
        if abs(lx_score - last_lx) < threshold:
            lx_score = (lx_score + last_lx) / 2
        last_lx = lx_score
    else:
        lx_score = last_lx  # If condition is not met, return the last score
    return lx_score, last_lx


def calculate_left_y_gaze_score(face_2d, last_ly, threshold):
    if (face_2d[23, 1] - face_2d[27, 1]) != 0:
        ly_score = (face_2d[468, 1] - face_2d[27, 1]) / (face_2d[23, 1] - face_2d[27, 1])
        if abs(ly_score - last_ly) < threshold:
            ly_score = (ly_score + last_ly) / 2
        last_ly = ly_score
    else:
        ly_score = last_ly  # If condition is not met, return the last score
    return ly_score, last_ly


def calculate_right_x_gaze_score(face_2d, last_rx, threshold):
    if (face_2d[359, 0] - face_2d[463, 0]) != 0:
        rx_score = (face_2d[473, 0] - face_2d[463, 0]) / (face_2d[359, 0] - face_2d[463, 0])
        if abs(rx_score - last_rx) < threshold:
            rx_score = (rx_score + last_rx) / 2
        last_rx = rx_score
    else:
        rx_score = last_rx  # If condition is not met, return the last score
    return rx_score, last_rx


def calculate_right_y_gaze_score(face_2d, last_ry, threshold):
    if (face_2d[253, 1] - face_2d[257, 1]) != 0:
        ry_score = (face_2d[473, 1] - face_2d[257, 1]) / (face_2d[253, 1] - face_2d[257, 1])
        if abs(ry_score - last_ry) < threshold:
            ry_score = (ry_score + last_ry) / 2
        last_ry = ry_score
    else:
        ry_score = last_ry  # If condition is not met, return the last score
    return ry_score, last_ry


def interpret_gaze_direction(lx_score, ly_score, rx_score, ry_score):
    # Calculate the average scores for more stable direction
    avg_x_score = (lx_score + rx_score) / 2
    avg_y_score = (ly_score + ry_score) / 2

    # Define thresholds for detecting direction
    # These thresholds may need adjustment based on testing
    x_threshold = 0.5  # Neutral threshold for x, adjust based on sensitivity needed
    y_threshold = 0.55  # Neutral threshold for y, adjust based on sensitivity needed

    if avg_x_score < x_threshold:
        x_direction = 'Looking Left'
    elif avg_x_score > x_threshold:
        x_direction = 'Looking Right'
    else:
        x_direction = 'Center'

    if avg_y_score < y_threshold:
        y_direction = 'Looking Up'
    elif avg_y_score > y_threshold:
        y_direction = 'Looking Down'
    else:
        y_direction = 'Center'

    return x_direction, y_direction


def move_mouse_based_on_gaze(x_direction, y_direction):
    move_distance = 10  # Adjust based on how much you want the mouse to move

    current_mouse_x, current_mouse_y = pyautogui.position()  # Get current mouse position

    if x_direction == 'Looking Left':
        new_x = current_mouse_x - move_distance
    elif x_direction == 'Looking Right':
        new_x = current_mouse_x + move_distance
    else:
        new_x = current_mouse_x

    if y_direction == 'Looking Up':
        new_y = current_mouse_y - move_distance
    elif y_direction == 'Looking Down':
        new_y = current_mouse_y + move_distance
    else:
        new_y = current_mouse_y

    pyautogui.moveTo(new_x, new_y)


def estimate_gaze_point_on_screen(lx_score, ly_score, rx_score, ry_score):
    screen_width, screen_height = pyautogui.size()

    # Calculate average scores and map to screen coordinates
    avg_x_score = (lx_score + rx_score) / 2
    gaze_x = int(avg_x_score * screen_width)
    avg_y_score = (ly_score + ry_score) / 2
    gaze_y = int(avg_y_score * screen_height)

    # Add the current gaze point to the deques
    gaze_points_x.append(gaze_x)
    gaze_points_y.append(gaze_y)

    # Calculate the moving average of the gaze points
    smooth_gaze_x = sum(gaze_points_x) // len(gaze_points_x)
    smooth_gaze_y = sum(gaze_points_y) // len(gaze_points_y)

    return smooth_gaze_x, smooth_gaze_y


def project_and_draw_axis(img, corner, rvec, tvec, cam_matrix, dist_coeffs, draw_headpose, draw_full_axis, draw_gaze,
                          color_headpose=(200, 200, 0), color_gaze=(0, 0, 255)):
    axis = np.float32([[-100, 0, 0], [0, 100, 0], [0, 0, 300]]).reshape(-1, 3)
    axis_projected, _ = cv2.projectPoints(axis, rvec, tvec, cam_matrix, dist_coeffs)

    if draw_headpose:
        if draw_full_axis:
            cv2.line(img, corner, tuple(np.ravel(axis_projected[0]).astype(np.int32)), color_headpose, 3)
            cv2.line(img, corner, tuple(np.ravel(axis_projected[1]).astype(np.int32)), (0, 200, 0), 3)
        cv2.line(img, corner, tuple(np.ravel(axis_projected[2]).astype(np.int32)), (0, 200, 200), 3)

    if draw_gaze:
        if draw_full_axis:
            cv2.line(img, corner, tuple(np.ravel(axis_projected[0]).astype(np.int32)), color_gaze, 3)
            cv2.line(img, corner, tuple(np.ravel(axis_projected[1]).astype(np.int32)), (0, 255, 0), 3)
        cv2.line(img, corner, tuple(np.ravel(axis_projected[2]).astype(np.int32)), color_gaze, 3)


while cap.isOpened():
    success, img = prepare_image_for_face_mesh(cap)

    if not success:
        continue

    img, face_2d, results = process_image_with_face_mesh(img, face_mesh)

    (img_h, img_w, img_c) = img.shape

    if not results.multi_face_landmarks:
        continue

    for face_landmarks in results.multi_face_landmarks:
        face_2d = convert_landmarks_to_pixel_coordinates(face_landmarks, img_w, img_h)

        # Get relevant landmarks for headpose estimation
        face_2d_head = np.array([
            face_2d[1],  # Nose
            face_2d[199],  # Chin
            face_2d[33],  # Left eye left corner
            face_2d[263],  # Right eye right corner
            face_2d[61],  # Left mouth corner
            face_2d[291]  # Right mouth corner
        ], dtype=np.float64)

        face_2d = np.asarray(face_2d)

        # Calculate left x gaze score
        lx_score, last_lx = calculate_left_x_gaze_score(face_2d, last_lx, threshold)

        # Calculate left y gaze score
        ly_score, last_ly = calculate_left_y_gaze_score(face_2d, last_ly, threshold)

        # Calculate right x gaze score
        rx_score, last_rx = calculate_right_x_gaze_score(face_2d, last_rx, threshold)

        # Calculate right y gaze score
        ry_score, last_ry = calculate_right_y_gaze_score(face_2d, last_ry, threshold)

        # Interpret and print gaze direction
        # x_direction, y_direction = interpret_gaze_direction(lx_score, ly_score, rx_score, ry_score)
        # print(f"Gaze Direction: {x_direction}, {y_direction}")
        # move_mouse_based_on_gaze(x_direction, y_direction)

        gaze_x, gaze_y = estimate_gaze_point_on_screen(lx_score, ly_score, rx_score, ry_score)
        print(f"Estimated Gaze Point: {gaze_x}, {gaze_y}")
        pyautogui.moveTo(gaze_x, gaze_y)

        # The camera matrix
        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, img_h / 2],
                               [0, focal_length, img_w / 2],
                               [0, 0, 1]])

        # Distortion coefficients
        dist_coeffs = np.zeros((4, 1), dtype=np.float64)

        # Solve PnP
        _, l_rvec, l_tvec = cv2.solvePnP(leye_3d, face_2d_head, cam_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
        _, r_rvec, r_tvec = cv2.solvePnP(reye_3d, face_2d_head, cam_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

        # Get rotational matrix from rotational vector
        l_rmat, _ = cv2.Rodrigues(l_rvec)
        r_rmat, _ = cv2.Rodrigues(r_rvec)

        # [0] changes pitch
        # [1] changes roll
        # [2] changes yaw
        # +1 changes ~45 degrees (pitch down, roll tilts left (counterclockwise), yaw spins left (counterclockwise))

        # Adjust headpose vector with gaze score
        l_gaze_rvec = np.array(l_rvec)
        l_gaze_rvec[2][0] -= (lx_score - .5) * x_score_multiplier
        l_gaze_rvec[0][0] += (ly_score - .5) * y_score_multiplier

        r_gaze_rvec = np.array(r_rvec)
        r_gaze_rvec[2][0] -= (rx_score - .5) * x_score_multiplier
        r_gaze_rvec[0][0] += (ry_score - .5) * y_score_multiplier

        # --- Projection ---

        # Get left and right eye corners as integers
        l_corner = face_2d_head[2].astype(np.int32)
        r_corner = face_2d_head[3].astype(np.int32)

        # Project and draw axis for the left eye
        # project_and_draw_axis(img, l_corner, l_rvec, l_tvec, cam_matrix, dist_coeffs, draw_headpose, draw_full_axis,
        #                       draw_gaze)

        # For the gaze direction, use the gaze rotation vector (l_gaze_rvec, r_gaze_rvec)
        project_and_draw_axis(img, l_corner, l_gaze_rvec, l_tvec, cam_matrix, dist_coeffs, False, draw_full_axis,
                              draw_gaze, color_gaze=(255, 0, 0))

        # # Repeat for the right eye
        # project_and_draw_axis(img, r_corner, r_rvec, r_tvec, cam_matrix, dist_coeffs, draw_headpose, draw_full_axis,
        #                       draw_gaze)

        # # And for the gaze direction of the right eye
        project_and_draw_axis(img, r_corner, r_gaze_rvec, r_tvec, cam_matrix, dist_coeffs, False, draw_full_axis,
                              draw_gaze, color_gaze=(255, 0, 0))

    cv2.imshow('Head Pose Estimation', img)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

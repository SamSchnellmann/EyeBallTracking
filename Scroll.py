import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import tkinter as tk
import threading
import time

# Variable to track the last time 'toggle_mode' was called
last_toggle_time = 0

last_blink_time = 0

left_eye_open = True

right_eye_open = True

blink_interval = 0

left_blink_list = []
right_blink_list = []
blink_list = []

left_blink_interval = 0

right_blink_interval = 0

# Set the scroll sensitivity
SCROLL_SENSITIVITY = 50

# Set mouse sensitivity
MOUSE_SENSITIVITY = 2

# Get the screen width and height
screen_width, screen_height = pyautogui.size()

# Global variable to track the current mode
current_mode = "MOUSE"  # Can be "MOUSE" or "SCROLL"


# Toggle mode based on facial gesture
def toggle_mode():
    global current_mode
    current_mode = "SCROLL" if current_mode == "MOUSE" else "MOUSE"
    show_notification_async(f"Switched to {current_mode} mode", duration=3000)


def show_notification(message, duration=3000):
    root = tk.Tk()
    root.title("Notification")
    label = tk.Label(root, text=message, font=('Helvetica', 10))
    label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
    # Set the window position
    root.geometry("+{}+{}".format(100, 100))
    # Make the window appear above other windows
    root.lift()
    root.attributes('-topmost', True)
    root.after(duration, root.destroy)  # Schedule the window to close after 'duration' milliseconds
    root.mainloop()


def show_notification_async(message, duration=3000):
    threading.Thread(target=show_notification, args=(message, duration)).start()


def initialize():
    mp_face_mesh = mp.solutions.face_mesh
    global face_mesh
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks = True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    global mp_drawing
    mp_drawing = mp.solutions.drawing_utils

    global drawing_spec
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    global cap
    cap = cv2.VideoCapture(1)


def process_image():
    success, image = cap.read()
    if not success:
        return None

    # Flip the image horizontally for a later selfie-view display
    # Also convert the color space from BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    image.flags.writeable = False

    # Get the result
    results = face_mesh.process(image)

    # To improve performance
    image.flags.writeable = True

    # Convert the color space from RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return image, results

def check_if_scroll(y):
    global scroll_queue 
    scroll_queue = [] 

    if len(scroll_queue) < 30:
        scroll_queue.append(y)
    else:
        scroll_queue.pop(0)
        scroll_queue.append(y)

def if_hit_gate(y):
    global new_gate

    global previous_gate

def handle_mouse(x, adjusted_mouse_dx, adjusted_mouse_dy, mode, scroll_direction):

    # Either moves the mouse in the direction of gaze or scrolls depending on vertical gaze
    if mode == "MOUSE":
        pyautogui.moveRel(adjusted_mouse_dx, adjusted_mouse_dy, duration=0.1)
    elif mode == "SCROLL":
        if(x > 0):
            pyautogui.scroll(SCROLL_SENSITIVITY)
        elif(x < 0):
            pyautogui.scroll(-SCROLL_SENSITIVITY)

# Function for handling left and right eye blinks to clicks
def handle_click(landmarks):

    # Declaring globals
    global left_eye_open
    global right_eye_open

    global left_blink_interval
    global right_blink_interval

    global left_blink_list
    global right_blink_list

    
    left_eye = [landmarks[159], landmarks[145]]
    right_eye = [landmarks[386], landmarks[374]]

    # Assigning left and right eye landmark current values
    top_lex, top_ley = (1000 * left_eye[0].x), (1000 * left_eye[0].y)
    bottom_lex, bottom_ley = (1000 * left_eye[1].x) , (1000 * left_eye[1].y)

    top_rex, top_rey = (1000 * right_eye[0].x), (1000 * right_eye[0].y)
    bottom_rex, bottom_rey = (1000 * right_eye[1].x), (1000 * right_eye[1].y)

    # If statements that append data to an array for every either eye is closed
    if(abs(top_ley - bottom_ley) < 6 ):

        left_blink_list.append("left")
        if(left_eye_open):
            left_blink_interval = time.time()
            left_eye_open = False
    else:
        left_eye_open = True

    if(abs(top_rey - bottom_rey) < 6 ):

        right_blink_list.append("right")
        if(right_eye_open):
            right_blink_interval = time.time()
            right_eye_open = False
    else:
        right_eye_open = True

    
    # Statements that empty array and perform click if 
    # Either list has more than 3 items in them
    if(left_blink_list.count('left') > 3):
        pyautogui.click(button = 'left')
        left_blink_interval = time.time()
        left_blink_list.clear()
    elif(left_eye_open == True):
        left_blink_interval = time.time()
        left_blink_list.clear()

    if(right_blink_list.count('right') > 3):
        pyautogui.click(button = 'right')
        right_blink_interval = time.time()
        right_blink_list.clear()
    elif(right_eye_open == True):
        right_blink_interval = time.time()
        right_blink_list.clear()


# def handle_back(landmarks, threshold=30):

#     pass

def handle_face_direction(x, y, adjusted_mouse_dx, adjusted_mouse_dy):
    text = "Forward"  # Default text

    # Determining gaze direction, setting text and calling handle mouse
    if y < -10:
        text = "Looking Left"
        handle_mouse(x, adjusted_mouse_dx, adjusted_mouse_dy, current_mode, 0)
    elif y > 10:
        text = "Looking Right"
        handle_mouse(x, adjusted_mouse_dx, adjusted_mouse_dy, current_mode, 0)
    elif x < 0:
        text = "Looking Down"
        handle_mouse(x, adjusted_mouse_dx, adjusted_mouse_dy, current_mode, -1)
    elif x > 10:
        text = "Looking Up"
        handle_mouse(x, adjusted_mouse_dx, adjusted_mouse_dy, current_mode, 1)

    return text


def check_mouth_open(landmarks, threshold=0.01):
    global last_toggle_time  # Use the global variable to track the last toggle time
    cooldown_period = 5  # Cooldown period in seconds

    # Example landmarks in MediaPipe, you may need to adjust based on actual indices
    upper_lip = landmarks[13]  # Adjust index as necessary
    lower_lip = landmarks[14]  # Adjust index as necessary

    # Calculate the vertical distance between the upper and lower lip
    mouth_open_distance = abs(upper_lip.y - lower_lip.y)

    current_time = time.time()
    if mouth_open_distance > threshold and (current_time - last_toggle_time) > cooldown_period:
        # print("Mouth Open")
        toggle_mode()
        last_toggle_time = current_time  # Update the last toggle time
        return True

    # print("Mouth Closed")
    return False


def draw_landmarks(image, results):
    img_h, img_w, _ = image.shape
    face_3d = []
    face_2d = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    # Get the 2D Coordinates
                    face_2d.append([x, y])

                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            # The camera matrix
            focal_length = 1 * img_w
            cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                   [0, focal_length, img_w / 2],
                                   [0, 0, 1]])

            # The distortion parameters
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Solve PnP
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            # Get rotational matrix
            rmat, jac = cv2.Rodrigues(rot_vec)

            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            # Get the y rotation degree
            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360

            mouse_dx = y * MOUSE_SENSITIVITY
            mouse_dy = -x * MOUSE_SENSITIVITY  # Inverting x because screen coordinates go from top to bottom

            # Get current mouse position
            current_mouse_x, current_mouse_y = pyautogui.position()

            # Calculate new position and adjust if it goes out of bounds
            new_mouse_x = current_mouse_x + mouse_dx
            new_mouse_y = current_mouse_y + mouse_dy

            # Ensure new mouse position is within screen bounds
            new_mouse_x = min(max(new_mouse_x, 0), screen_width)
            new_mouse_y = min(max(new_mouse_y, 0), screen_height)

            # Calculate adjusted mouse movement
            adjusted_mouse_dx = new_mouse_x - current_mouse_x
            adjusted_mouse_dy = new_mouse_y - current_mouse_y

            text = handle_face_direction(x, y, adjusted_mouse_dx, adjusted_mouse_dy)

            if current_mode == "MOUSE":
                handle_click(face_landmarks.landmark)

            check_mouth_open(face_landmarks.landmark)

            # Display the nose direction
            cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

            cv2.line(image, p1, p2, (255, 255, 0), 3)

            for land in face_landmarks.landmark:
                x1 = int(land.x * image.shape[1])
                y1 = int(land.y * image.shape[0])
                cv2.circle(image, (x1, y1), 3, (0, 255, 255))

        

            # Add the text on the image
            cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            cv2.putText(image, "x: " + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "y: " + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


def main():
    initialize()
    while cap.isOpened():
        processed_image = process_image()
        if processed_image is None:
            break
        image, results = processed_image
        draw_landmarks(image, results)
        cv2.imshow('Head Pose Estimation', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

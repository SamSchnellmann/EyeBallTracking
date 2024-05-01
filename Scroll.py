import cv2
import mediapipe as mp
import numpy as np
import math
import pyautogui
import tkinter as tk
import threading
import time

pyautogui.FAILSAFE = False

# Global variables initialization
# Track the last time the mode was toggled
last_toggle_time = 0

last_back_time = 0

last_blink_time = 0

left_eye_open = True

right_eye_open = True

blink_interval = 0

left_blink_list = []
right_blink_list = []
blink_list = []

# Set the scroll sensitivity
SCROLL_SENSITIVITY = 50

# Track time intervals between blinks
left_blink_time = 0
right_blink_time = 0

# Configuration for interaction sensitivity
SCROLL_SENSITIVITY = 50  # Defines the amount of scroll per scroll event
MOUSE_SENSITIVITY = 2  # Defines how much the mouse moves in response to head movement

# Fetch the screen dimensions to manage GUI elements appropriately
screen_width, screen_height = pyautogui.size()

# A global variable to hold the current interaction mode; affects how gestures control the cursor
current_mode = "MOUSE"  # Can be "MOUSE" or "SCROLL"


def toggle_mode():
    """
    Toggles the control mode between "MOUSE" and "SCROLL".

    This function switches the operational mode of the application between mouse control and scrolling control,
    based on the current state. It also triggers a notification to the user about the mode change.

    Effects:
        - Updates the global `current_mode` variable to the next mode.
        - Calls `show_notification_async` to display a mode change notification on the screen.
    """
    global current_mode
    current_mode = "SCROLL" if current_mode == "MOUSE" else "MOUSE"
    show_notification_async(f"Switched to {current_mode} mode", duration=1000)


def show_notification(message, duration=3000):
    """
    Displays a notification window with a specified message for a given duration.

    Args:
    message (str): The message to display in the notification window.
    duration (int): How long the notification should stay open, in milliseconds.

    This function creates a simple GUI window using Tkinter to show a temporary message to the user.
    It sets the window as a topmost window so it stays above all other windows and closes automatically
    after the specified duration.
    """
    root = tk.Tk()
    root.title("Notification")
    label = tk.Label(root, text=message, font=('Helvetica', 10))
    label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
    root.geometry("+{}+{}".format(100, 100))  # Positions the window at screen coordinates (100, 100)
    root.lift()
    root.attributes('-topmost', True)  # Keeps the window above all other windows
    root.after(duration, root.destroy)  # Automatically closes the window after 'duration' milliseconds
    root.mainloop()


def show_notification_async(message, duration=3000):
    """
    Displays a notification asynchronously.

    Args:
    message (str): The message to be displayed in the notification.
    duration (int): Duration in milliseconds for which the notification should be visible.

    This function starts a new thread to display the notification without blocking the main program execution.
    This is particularly useful for non-blocking UI updates in a multi-threaded application.
    """
    threading.Thread(target=show_notification, args=(message, duration)).start()


def initialize():
    """
    Initializes necessary components for facial mesh processing and webcam access.

    This function sets up the MediaPipe face mesh solution with specified configurations for better landmark detection.
    It also attempts to connect to a webcam by checking available camera indices. Raises an exception if no camera is found.

    Global Variables:
    face_mesh (mp.solutions.face_mesh.FaceMesh): A MediaPipe FaceMesh object configured for the application.
    mp_drawing (mp.solutions.drawing_utils): MediaPipe drawing utilities.
    drawing_spec (mp.solutions.drawing_utils.DrawingSpec): Drawing specifications for landmarks.
    cap (cv2.VideoCapture): The OpenCV video capture object linked to the webcam.
    """
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
    """
    Captures an image from the webcam, processes it for facial landmark detection, and prepares it for further analysis.

    Returns:
    tuple: A tuple containing the processed image and the results of the facial landmark detection, or
           None if the webcam fails to capture an image.

    This function reads an image from the webcam, flips it for a mirror view, converts the color from BGR to RGB,
    processes it using MediaPipe's face mesh to detect facial landmarks, and converts it back to BGR for display.
    The image data is temporarily made non-writable to improve performance during processing.
    """
    success, image = cap.read()
    if not success:
        return None

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)
    image.flags.writeable = True
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


def handle_mouse(x, adjusted_mouse_dx, adjusted_mouse_dy, mode):

    """
    Specific function for either scrolling up or down or moving the mouse depending
    on which mode the program is in.
    """

    # Either moves the mouse in the direction of gaze or scrolls depending on vertical gaze
    if mode == "MOUSE":
        pyautogui.moveRel(adjusted_mouse_dx, adjusted_mouse_dy, duration=0.1)
    elif mode == "SCROLL":
        if(x > 0):
            pyautogui.scroll(SCROLL_SENSITIVITY)
        elif(x < 0):
            pyautogui.scroll(-SCROLL_SENSITIVITY)





def handle_back_forth(image, landmarks):

        global last_back_time
        
        interval = 1.5
    
        top = landmarks[10]
        bottom = landmarks[152]

        direction = ''

        current_time = time.time()

        t = (top.x * math.ceil(image.shape[1]), top.y * math.ceil(image.shape[0]))
        b = (bottom.x * math.ceil(image.shape[1]), bottom.y * math.ceil(image.shape[0]))

        angle = np.arctan2(t, b)

        if(angle[0] < 0.7 and (current_time - last_back_time) > interval):
            direction = 'left'

        if(angle[0] > 0.86 and (current_time - last_back_time) > interval):
            direction = 'right'
        
        if(direction):
            pyautogui.keyDown('alt')
            pyautogui.press(direction)
            pyautogui.keyUp('alt')
            last_back_time = current_time



# Function for handling left and right eye blinks to clicks
def handle_click(landmarks):

    # Declaring globals
    global left_eye_open
    global right_eye_open

    global left_blink_time
    global right_blink_time

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
    if(abs(top_ley - bottom_ley) < 6 and abs(top_lex - bottom_lex) < 6):

        left_blink_list.append("left")
        if(left_eye_open):
            left_blink_time = time.time()
            left_eye_open = False
    else:
        left_eye_open = True

    if(abs(top_rey - bottom_rey) < 6 and abs(top_rex - bottom_rex) < 6):

        right_blink_list.append("right")
        if(right_eye_open):
            right_blink_time = time.time()
            right_eye_open = False
    else:
        right_eye_open = True

    
    # Statements that empty array and perform click if 
    # Either list has more than 3 items in them
    if(left_blink_list.count('left') > 3):
        pyautogui.click(button = 'left')
        left_blink_time = time.time()
        left_blink_list.clear()
    elif(left_eye_open == True):
        left_blink_time = time.time()
        left_blink_list.clear()

    if(right_blink_list.count('right') > 3):
        pyautogui.click(button = 'right')
        right_blink_time = time.time()
        right_blink_list.clear()
    elif(right_eye_open == True):
        right_blink_time = time.time()
        right_blink_list.clear()



def handle_face_direction(x, y, adjusted_mouse_dx, adjusted_mouse_dy):
    """
    Determines what direction the user is looking based on the X and Y values
    of the vector point generated by their facial landmark data.

    When the program determines the user is looking in a given direction, it calls
    the handle_mouse function which will move the user's mouse cursor in the direction
    they are looking depending on how much in a given direction they are looking.
    """

    threshold = 7
    
    look_text = "Looking"

    default_text = "Forward"  

    # Determining gaze direction, setting text and calling handle mouse
    if y < -threshold:
        look_text += " Left"
        adjusted_mouse_dx += threshold
    elif y > threshold:
        look_text += " Right"
        adjusted_mouse_dx -= threshold

    if x < 0:
        look_text += " Down"
        adjusted_mouse_dy *= 1.3
    elif x > threshold:
        look_text += " Up"
        adjusted_mouse_dy += threshold

    if len(look_text) > 7:
        handle_mouse(x, adjusted_mouse_dx, adjusted_mouse_dy, current_mode)
        return look_text

    return default_text


def check_mouth_open(landmarks, threshold=0.01):
    """
    Checks if the mouth is open beyond a specified threshold and toggles the mode if conditions are met.

    Args:
    landmarks (list): A list of facial landmarks detected.
    threshold (float): The distance threshold at which the mouth is considered open.

    Returns:
    bool: True if the mouth is open beyond the threshold and a mode toggle occurs, False otherwise.

    This function checks the vertical distance between the upper and lower lip landmarks to determine
    if the mouth is open wide enough. If the mouth has been open beyond the threshold for a longer period
    than the cooldown, the function toggles the current mode and updates the last toggle time.
    """
    global last_toggle_time  # Use the global variable to track the last toggle time
    cooldown_period = 1  # Cooldown period in seconds to prevent rapid toggling

    # Extract the upper and lower lip positions
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
    """
    Draws facial landmarks and head pose vectors on the image based on detection results.

    Args:
    image (np.array): The image on which landmarks and vectors will be drawn.
    results (object): The results object containing multi-face landmarks detected by MediaPipe.

    Processes detected facial landmarks to calculate and display the 2D and 3D positions of significant points
    like the nose. It also calculates head pose angles and projects these onto the image to visualize the direction
    the user's head is facing. This function modifies the input image by drawing lines and text indicating head
    direction and landmark positions.

    The function integrates several steps:
    - Extracting 2D and 3D coordinates of specific landmarks.
    - Calculating the head pose using solvePnP.
    - Projecting head direction as a line on the image.
    - Displaying text annotations for head pose angles and other diagnostics.

    It adjusts the mouse control based on the head pose and triggers actions based on facial gestures like mouth opening.
    """
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

            handle_back_forth(image, face_landmarks.landmark)

            # Display the nose direction
            cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

            p1 = (int(nose_2d[0]), int(nose_2d[1]))
            p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

            cv2.line(image, p1, p2, (255, 255, 0), 3)

            # for land in face_landmarks.landmark:
            #     x1 = int(land.x * image.shape[1])
            #     y1 = int(land.y * image.shape[0])
            #     cv2.circle(image, (x1, y1), 3, (0, 255, 255))

        

            # Add the text on the image
            cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            cv2.putText(image, "x: " + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "y: " + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


def main():
    """
    Main function to initialize and run the facial tracking application.

    This function encapsulates the primary application loop and is responsible for:
    - Initializing the system resources and camera.
    - Capturing images from the camera and processing them to detect and visualize facial landmarks.
    - Displaying the processed images with annotations.
    - Handling user input to gracefully exit the application.

    The function tries to initialize the application and handles any exceptions that occur during initialization.
    If the camera is successfully opened, it enters a loop where it continuously processes the images captured
    from the camera. It displays these images and checks for a quit command. If an exit is requested or if no more
    images are received (camera closed), it cleans up by releasing camera resources and closing any GUI windows.
    """
    try:
        initialize()  # Initialize the camera and face mesh processing
    except Exception as e:
        print(e)  # Print any errors that occur during initialization and exit
        return

    while cap.isOpened():  # Continue as long as the camera is open
        processed_image = process_image()  # Process each image to detect facial features
        if processed_image is None:  # If no image is returned, exit the loop
            break
        image, results = processed_image
        draw_landmarks(image, results)  # Draw landmarks and other visual elements on the image
        cv2.imshow('Head Pose Estimation', image)  # Display the annotated image
        if cv2.waitKey(5) & 0xFF == 27:  # Exit if the ESC key is pressed
            break

    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows


if __name__ == "__main__":
    main()

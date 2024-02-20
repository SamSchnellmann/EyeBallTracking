import pyautogui  # Import the PyAutoGUI library for controlling the mouse cursor.
import screen_utils as su
import face_utils as fu
import eye_utils as eu

# Get the screen width and height using PyAutoGUI.
screen_w, screen_h = su.screen_size()


def move_cursor_to_landmark(landmark):
    """
    Move the mouse cursor to the specified landmark position.

    Parameters:
    - landmark (Landmark): The landmark point to move the cursor to.

    Returns:
    - None
    """
    screen_x = int(screen_w * landmark.x)
    screen_y = int(screen_h * landmark.y)
    pyautogui.moveTo(screen_x, screen_y)


def iris_mouse(landmarks, frame):
    """
    Move the cursor to the second iris landmark.

    Parameters:
    - landmarks (list): List of detected landmarks.
    - frame (numpy.ndarray): The input frame (image) to draw the landmark on.

    Returns:
    - None
    """
    iris_landmarks = eu.find_iris_landmarks(landmarks)
    for id, landmark in enumerate(iris_landmarks):

        #Draws the frame around the right eye
        fu.draw_face_landmark(frame, landmark, (0, 255, 0))
        if id == 1:
            move_cursor_to_landmark(landmark)

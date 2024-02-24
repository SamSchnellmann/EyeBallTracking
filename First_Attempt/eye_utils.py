import face_utils as fu
import pyautogui  # Import the PyAutoGUI library for controlling the mouse cursor.


def blink(landmarks, frame):
    """
    Find blink landmarks and perform a click action if the blink condition is met.

    Parameters:
    - landmarks (list): List of detected landmarks.
    - frame (numpy.ndarray): The input frame (image) to draw the landmark on.

    Returns:
    - None
    """
    if len(landmarks) >= 160:
        left = [landmarks[145], landmarks[159]]
        right = [landmarks[33], landmarks[133]]
        for landmark in right:
            fu.draw_face_landmark(frame, landmark, (0, 0, 255))
        for landmark in left:
            fu.draw_face_landmark(frame, landmark, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.01:
            pyautogui.click()
            pyautogui.sleep(1)


def find_iris_landmarks(landmarks):
    """
    Find iris landmarks.

    Parameters:
    - landmarks (list): List of detected landmarks.

    Returns:
    - iris_landmarks (list): List of iris landmarks if available, otherwise an empty list.
    """
    iris_landmarks = []
    if len(landmarks) >= 478:
        iris_landmarks = landmarks[474:478]
    return iris_landmarks

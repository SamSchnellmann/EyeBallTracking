import mediapipe as mp  # Import the MediaPipe library for face detection and landmark estimation.
import cv2  # Import the OpenCV library for image processing.


def get_face_marks():
    """
    Detect landmarks on the provided frame.

    Parameters:
    - none

    Returns:
    - landmark_points (list): A list containing the detected landmark points if any faces are detected
    """
    return mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)


def detect_face_landmarks(frame):
    """
    Detect landmarks on the provided frame.

    Parameters:
    - frame (numpy.ndarray): The input frame (image) in BGR color format.

    Returns:
    - landmark_points (list): A list containing the detected landmark points if any faces are detected, else None.
    """
    # Convert the frame from BGR to RGB color format for compatibility with MediaPipe.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the RGB frame to detect faces and estimate landmarks using FaceMesh.
    output = get_face_marks().process(rgb_frame)
    # Retrieve the detected landmark points from the output.
    landmark_points = output.multi_face_landmarks
    return landmark_points


def draw_face_landmark(frame, landmark, color):
    """
    Draw a landmark on the provided frame.

    Parameters:
    - frame (numpy.ndarray): The input frame (image) to draw the landmark on.
    - landmark (Landmark): The landmark point to be drawn.
    - color (tuple): The color of the drawn landmark.

    Returns:
    - None
    """
    # Calculate the pixel coordinates of the landmark on the frame.
    x = int(landmark.x * frame.shape[1])
    y = int(landmark.y * frame.shape[0])
    # Draw a circle around the landmark on the frame.
    cv2.circle(frame, (x, y), 3, color)

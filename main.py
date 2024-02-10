import cv2  # Import the OpenCV library for image processing.
import mediapipe as mp  # Import the MediaPipe library for face detection and landmark estimation.
import pyautogui  # Import the PyAutoGUI library for controlling the mouse cursor.
import face_utils as fu
import mouse_utils as mu
import eye_utils as eu


def process_video_stream(cam):
    """
    Process the video stream, detect facial landmarks, and control the mouse cursor accordingly.

    Parameters:
    - cam (cv2.VideoCapture): The OpenCV VideoCapture object representing the camera.

    Returns:
    - None
    """
    while True:
        # Read a frame from the camera.
        ret, frame = cam.read()
        # If there's an issue reading the frame, break out of the loop.
        if not ret:
            break
        # Flip the frame horizontally for a mirrored view.
        frame = cv2.flip(frame, 1)
        # Detect landmarks on the frame.
        landmark_points = fu.detect_face_landmarks(frame)
        # If any landmarks are detected:
        if landmark_points:
            # Get the landmarks of the first face detected.
            landmarks = landmark_points[0].landmark
            # Call the function to find iris landmarks and move cursor.
            mu.iris_mouse(landmarks, frame)
            # Call the function to find blink landmarks and perform click action.
            eu.blink(landmarks, frame)
        # Display the processed frame with annotations.
        cv2.imshow('Eye Controlled Mouse', frame)
        # Check for the 'q' key press to exit the loop.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows.
    cam.release()
    cv2.destroyAllWindows()


# Initialize the camera for capturing video frames.
cam = cv2.VideoCapture(0)
# Call the function to process the video stream.
process_video_stream(cam)

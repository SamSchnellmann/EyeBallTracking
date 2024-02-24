# "Gaze Locking: Passive Eye Contact Detection for Human?Object Interaction,"
# B.A. Smith, Q. Yin, S.K. Feiner and S.K. Nayar,
# ACM Symposium on User Interface Software and Technology (UIST),
# pp. 271-280, Oct. 2013.

import cv2
import mediapipe as mp
import math
import numpy as np
import pyautogui

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,  # Enables iris detection
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# Initialize drawing utils for visualization
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


# Function to calculate distance between two points in pixel space
def calculate_distance(landmark1, landmark2, image_width, image_height):
    x1, y1 = landmark1.x * image_width, landmark1.y * image_height
    x2, y2 = landmark2.x * image_width, landmark2.y * image_height
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Function to estimate distance based on iris size change
def estimate_distance(iris_diameter_pixels):
    calibration_distance_cm = 30  # Known distance from camera during calibration in cm
    calibration_diameter_pixels = 150  # Example value, adjust based on your calibration
    return calibration_distance_cm * (calibration_diameter_pixels / iris_diameter_pixels)


# Function to highlight eye landmarks
def draw_eye_landmarks(image, landmarks, eye_indices, image_width, image_height):
    for i in range(len(eye_indices) - 1):
        start_point = landmarks[eye_indices[i]]
        end_point = landmarks[eye_indices[i + 1]]
        cv2.line(image,
                 (int(start_point.x * image_width), int(start_point.y * image_height)),
                 (int(end_point.x * image_width), int(end_point.y * image_height)),
                 (0, 255, 0), 2)


# Function to calculate the center of the eye
def calculate_eye_center(eye_corner_left, eye_corner_right, image_width, image_height):
    eye_center_x = (eye_corner_left.x + eye_corner_right.x) * 0.5 * image_width
    eye_center_y = (eye_corner_left.y + eye_corner_right.y) * 0.5 * image_height
    return np.array([eye_center_x, eye_center_y])


# Function to calculate gaze vector
def calculate_gaze_vector(eye_center, iris_center):
    gaze_vector = iris_center - eye_center
    return gaze_vector / np.linalg.norm(gaze_vector)


# Define calibration points on the screen
def get_calibration_points(screen_width, screen_height):
    return [
        (int(screen_width * 0.1), int(screen_height * 0.1)),
        (int(screen_width * 0.5), int(screen_height * 0.1)),
        (int(screen_width * 0.9), int(screen_height * 0.1)),
        (int(screen_width * 0.1), int(screen_height * 0.5)),
        (int(screen_width * 0.5), int(screen_height * 0.5)),
        (int(screen_width * 0.9), int(screen_height * 0.5)),
        (int(screen_width * 0.1), int(screen_height * 0.9)),
        (int(screen_width * 0.5), int(screen_height * 0.9)),
        (int(screen_width * 0.9), int(screen_height * 0.9))
    ]


# Function to display calibration points and capture gaze vectors
def run_screen_calibration(calibration_points, screen_width, screen_height):
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
    calibration_data = []

    for point in calibration_points:
        display_image = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
        cv2.circle(display_image, point, 50, (0, 255, 0), -1)  # Draw calibration point
        cv2.imshow("Calibration", display_image)
        cv2.waitKey(1000)  # Wait for a second to fixate gaze

        # Capture frame for gaze vector calculation
        success, image = cap.read()
        if not success:
            print("Failed to capture image")
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Example for one eye, replicate for the other eye as needed
                eye_corner_left = face_landmarks.landmark[133]  # Left eye left corner
                eye_corner_right = face_landmarks.landmark[33]  # Left eye right corner
                eye_center = calculate_eye_center(eye_corner_left, eye_corner_right, screen_width, screen_height)

                iris_center = np.array([face_landmarks.landmark[473].x * screen_width,
                                        face_landmarks.landmark[473].y * screen_height])  # Iris center landmark

                gaze_vector = calculate_gaze_vector(eye_center, iris_center)
                calibration_data.append((point, gaze_vector))

    cv2.destroyAllWindows()
    cap.release()
    return calibration_data


# Function to map gaze vectors to screen coordinates
def map_gaze_to_screen_coordinates(calibration_data, current_gaze_vector):
    # Find the calibration point with the closest gaze vector to the current gaze vector
    closest_point = None
    min_distance = float('inf')
    for point, gaze_vector in calibration_data:
        distance = np.linalg.norm(gaze_vector - current_gaze_vector)
        if distance < min_distance:
            min_distance = distance
            closest_point = point
    return closest_point


# Continuously capture the current gaze and map it to screen coordinates
def track_and_map_gaze(calibration_data, screen_width, screen_height):
    cap = cv2.VideoCapture(0)
    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                eye_corner_left = face_landmarks.landmark[133]  # Left eye
                eye_corner_right = face_landmarks.landmark[33]  # Right eye
                eye_center = calculate_eye_center(eye_corner_left, eye_corner_right, screen_width, screen_height)

                iris_center = np.array([face_landmarks.landmark[473].x * screen_width,
                                        face_landmarks.landmark[473].y * screen_height])

                current_gaze_vector = calculate_gaze_vector(eye_center, iris_center)
                screen_coordinates = map_gaze_to_screen_coordinates(calibration_data, current_gaze_vector)

                if screen_coordinates:
                    # Convert screen_coordinates to integers, as circle() requires integer coordinates
                    screen_coordinates = tuple(map(int, screen_coordinates))
                    # Drawing a black circle on the predicted gaze point
                    cv2.circle(image, screen_coordinates, 10, (0, 0, 0), -1)  # Changed color to black
                    cv2.imshow('Gaze Tracking', image)

                if cv2.waitKey(5) & 0xFF == 27:  # Break the loop with the 'ESC' key
                    break

    cap.release()
    cv2.destroyAllWindows()


# Main function to execute the calibration and start gaze tracking
def main():
    screen_width, screen_height = pyautogui.size()
    calibration_points = get_calibration_points(screen_width, screen_height)

    # Execute screen calibration
    calibration_data = run_screen_calibration(calibration_points, screen_width, screen_height)
    print("Calibration Data:", calibration_data)

    # After calibration, start tracking the gaze and map it to screen coordinates
    track_and_map_gaze(calibration_data, screen_width, screen_height)

if __name__ == "__main__":
    main()

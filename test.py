import cv2
import mediapipe as mp

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# Draw a circle and label at whatever landmark you want.
def draw_first_landmark(img, landmark, width, height):
    x = int(landmark.x * width)
    y = int(landmark.y * height)
    cv2.circle(img, (x, y), 7, (100, 100, 0), -1)
    cv2.putText(img, '0', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)


# Draw circles and labels for all landmarks
def draw_all_landmarks(img, face_landmarks, width, height):
    for i, landmark in enumerate(face_landmarks.landmark):
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(img, (x, y), 1, (100, 100, 0))
        # commented out because it will crowd out the screen
        # cv2.putText(img, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


# Draw irises
def draw_irises(img, face_landmarks):
    mp_drawing.draw_landmarks(
        image=img,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_IRISES,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
    )


# Draw face contours
def draw_face_contours(img, face_landmarks):
    mp_drawing.draw_landmarks(
        image=img,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
    )


# Draw tesselation (grid pattern) on face
def draw_tesselation(img, face_landmarks):
    mp_drawing.draw_landmarks(
        image=img,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
    )


# Function to initialize MediaPipe FaceMesh
def initialize_face_mesh():
    return mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)


# Function to initialize webcam
def initialize_webcam():
    return cv2.VideoCapture(0)


# Function to process the image with MediaPipe
def process_image(img, face_mesh):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return img_bgr, results


# Function to close webcam and destroy all windows
def close_webcam(webcam):
    webcam.release()
    cv2.destroyAllWindows()


# Function to run the main application loop
def run_application():
    webcam = initialize_webcam()
    face_mesh = initialize_face_mesh()

    while webcam.isOpened():
        success, img = webcam.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        height, width, _ = img.shape

        img_bgr, results = process_image(img, face_mesh)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                draw_first_landmark(img_bgr, face_landmarks.landmark[0], width, height)
                draw_all_landmarks(img_bgr, face_landmarks, width, height)
                draw_irises(img_bgr, face_landmarks)
                draw_face_contours(img_bgr, face_landmarks)
                draw_tesselation(img_bgr, face_landmarks)

        cv2.imshow("Testing", img_bgr)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    close_webcam(webcam)


# Call the main application loop function
if __name__ == "__main__":
    run_application()

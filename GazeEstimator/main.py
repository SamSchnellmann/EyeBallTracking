import mediapipe as mp
import cv2
import gaze
import userface

mp_face_mesh = mp.solutions.face_mesh  # initialize the face mesh model


# camera stream:
# cap = cv2.VideoCapture(0)  # chose camera index (try 1, 2, 3)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) 
# cap = cv2.VideoCapture('video2.mp4') 


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,  # number of faces to track in each frame
        refine_landmarks=True,  # includes iris landmarks in the face mesh model
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
        

    while cap.isOpened():

        success, image = cap.read()
        if not success:  # no frame input
            print("Ignoring empty camera frame.")
            continue

        # --Looking into what the guy who wrote this means by this--
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # frame to RGB for the face-mesh model
        results = face_mesh.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # frame back to BGR for OpenCV
        try:
            landmarks = results.multi_face_landmarks[0]
        except:
            cv2.imshow('output window', image)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
            continue
        frame_h, frame_w, _ = image.shape

        # Function for showing all landmarks

        # for land in landmarks.landmark:
        #     x1 = int(land.x * frame_w)
        #     y1 = int(land.y * frame_h)
        #     cv2.circle(image, (x1, y1), 3, (0, 255, 255))

        # Keybind for setting to calibrated mode
        if cv2.waitKey(1) & 0xFF == ord('p'):
            gaze.flag = 1

        # Keybind for setting back to un-calibrated
        if cv2.waitKey(1) & 0xFF == ord('s'):
            gaze.flag = None

        # Main gaze function call
        if results.multi_face_landmarks:
            gaze.gaze(image, results.multi_face_landmarks[0])  # gaze estimation
        else:
            print("No landmarks")
        

        cv2.imshow('output window', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
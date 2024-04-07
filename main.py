# will m
import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
# locate facial features/landmarks
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# detect screen size
screen_w, screen_h = pyautogui.size()

# define a sensitivity factor to increase sensitivity
SENSITIVITY_FACTOR = 2.0  # Adjust this value as needed

while True:
    # create window, use webcam
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)

    # convert video to different color
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)

    # detect if face is present or not, track location (x and y) in frame
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        # detecting eye, ignore other facial features
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                # Increase sensitivity by multiplying with sensitivity factor
                screen_x = screen_w / frame_w * x * SENSITIVITY_FACTOR
                screen_y = screen_h / frame_h * y * SENSITIVITY_FACTOR
                pyautogui.moveTo(screen_x, screen_y)

        # track top of eyelid, and bottom of eyelid to detect blink
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))

        # measure distance between top & bottom eyelid to detect blinking. <0.004 is distance
        # if true, click and wait 1s to prevent spam clicking
        if (left[0].y - left[1].y) < 0.01:
            pyautogui.click()
            pyautogui.sleep(1.0)

    # init frame & application name
    cv2.imshow('EyeMouse', frame)
    cv2.waitKey(1)

    # break the loop when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break


import cv2
import mediapipe as mp
import numpy as np
import torch
import csv


def main():
    # Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection()

    #Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()

    # Video stream 
    cap = cv2.VideoCapture(0)

    # CSV file for recording facial landmarks
    csv_filename = "facial_landmarks.csv"
    csv_file = open(csv_filename, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    # Landmarks are written in this sequence (x0, y0, z0, x1, y1, z1, x2, y2, z2....)
    # Landmarks need to be stored in a more readable format that places each set of landmarks into it's own row based on the arrays they're set up with in landmarks.py
    # Left Iris (x0, y0, z0, x1, y1, z1...)
    # Left Eye Outlinse (x0, y0, z0, x1, y1, z1...)
    # ...

    count = 0

    while True:
        count += 1
        
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB for processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face
        results_face = face_detection.process(rgb_frame)
        if results_face.detections:
            for detection in results_face.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Detect facial landmarks
                results_landmarks = face_mesh.process(rgb_frame)
                if results_landmarks.multi_face_landmarks:
                    landmarks = results_landmarks.multi_face_landmarks[0].landmark

                    # Convert landmarks to numpy array
                    landmarks_np = np.array([(landmark.x, landmark.y, landmark.z) for landmark in landmarks]).flatten()

                    # Write landmarks to CSV file
                    if count >= 30:
                        
                        csv_writer.writerow(landmarks_np)
                    count %= 30

        cv2.imshow("Face Detection", frame)

        # Break the loop with q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close CSV file
    cap.release()
    csv_file.close()

    # Close all OpenCV windows
    cv2.destroyAllWindows()


# Run main
if __name__ == "__main__":
    main()
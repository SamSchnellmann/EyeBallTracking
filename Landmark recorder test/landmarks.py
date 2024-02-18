#Mediapipe landmarks of interest 
    # Left eye: 469-472(iris) (33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7)(Outer Eye Outline)
    # Right eye: 473-477(iris) (263, 466, 388, 387, 386, 385, 384, 398, 362, 382, 381, 380, 374, 373, 390, 249)(Outer Eye Outline)
    # Nose: (4, 48, 278, 8, 2)
    # Face Outline: (103, 10, 132, 58, 288, 152, 235, 454)


left_eye_outline = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
rigth_eye_outline = [263, 466, 388, 387, 386, 385, 384, 398, 362, 382, 381, 380, 374, 373, 390, 249]
left_iris = [468, 469, 470, 471, 472]
right_iris = [473, 474, 475, 476, 477]
nose = [4, 48, 278, 8, 2]
face_outline = [103, 10, 132, 58, 288, 152, 235, 454]

def reduced_landmarks(landmarks):
    # Use this function to input the facial landmark array and return a 2d array of the individual landmark arrays above.
    # Then Write to the csv file with each row being labeled properly.
    print(":0")

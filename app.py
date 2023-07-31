import pickle
import cv2
import os
import cvzone
import face_recognition
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

# Graphics
imgBackground = cv2.imread('ressources/background.png')

# Importing mode images into a list
folderModePath = 'ressources/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    image_path = os.path.join(folderModePath, path)
    img_mode = cv2.imread(image_path)
    if img_mode is not None:
        imgModeList.append(img_mode)
    else:
        print(f"Failed to read image: {image_path}")

print(len(imgModeList))


# Load the encoding file
print('Loading EncodeFile ...')
file = open('venv/EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()

encodeListKnown , studentsIds = encodeListKnownWithIds
print(studentsIds)
print('EncodeFile loaded')


while True:
    success, img = cap.read()

    #smaller image & conversion
    imgS = cv2.resize(img,(0,0),None,0.25 ,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img

    # Check if imgModeList has at least one valid image before accessing it
    if len(imgModeList) > 0:
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]

    for encodeFace , faceLoc in zip(encodeCurFrame , faceCurFrame) :
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

        print("matches", matches)
        # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        #print("matchIndex", matchIndex)
        if matches[matchIndex] :
            print("known face detected")
            # print(studentsIds[matchIndex])
            # Get the scaled face coordinates
            y1, x2, y2, x1 = faceLoc
            y1_scaled, x2_scaled, y2_scaled, x1_scaled = y1 * 0.99, x2 * 0.99, y2 * 0.99, x1 * 0.99

            # Calculate the coordinates for the rectangle (bbox) based on the scaled face coordinates
            bbox = (55 + int(x1_scaled), 162 + int(y1_scaled), int(x2_scaled - x1_scaled), int(y2_scaled - y1_scaled))

            # Draw the green rectangle on the original image (imgBackground)
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)

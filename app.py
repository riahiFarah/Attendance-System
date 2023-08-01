import pickle
import cv2
import os
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred , {
    'databaseURL' : "your db URL here",
    'storageBucket' : "your storage URL here"
})

bucket = storage.bucket()



cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

# Graphics
imgBackground = cv2.imread('ressources/background.png')

# Importing mode images into a list
folderModePath = 'ressources/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
imgStudent = []
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


modeType = 0
counter = 0
id = -1

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
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace , faceLoc in zip(encodeCurFrame , faceCurFrame) :
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

        # print("matches", matches)
        # print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        #print("matchIndex", matchIndex)
        if matches[matchIndex] :
            # Create the image path
            # image_path = f'images/{id}.png'

            # print(f"Attempting to read image from path: {image_path}")

            # print("known face detected")
            # print(studentsIds[matchIndex])
            # Get the scaled face coordinates
            y1, x2, y2, x1 = faceLoc
            y1_scaled, x2_scaled, y2_scaled, x1_scaled = y1 * 0.99, x2 * 0.99, y2 * 0.99, x1 * 0.99

            # Calculate the coordinates for the rectangle (bbox) based on the scaled face coordinates
            bbox = (55 + int(x1_scaled), 162 + int(y1_scaled), int(x2_scaled - x1_scaled), int(y2_scaled - y1_scaled))

            # Draw the green rectangle on the original image (imgBackground)
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            id=studentsIds[matchIndex]
            if counter == 0 :
                counter = 1
                modeType = 1


    if counter != 0 :
        if counter ==1:
            # Get the users data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            # Get image from storage
            blob = bucket.get_blob(f'images/{id}.png')

            # Get image from the local file system
            # imgStudent = cv2.imread(image_path)

            if blob is None :
                print('blob is none')

            if blob is not None:  # Check if the blob exists before attempting to download

                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                if imgStudent is not None and imgStudent.shape[0] != 0:
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                    counter += 1

                else:
                    print(f"Failed to download or decode image for student ID {id}")
        cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

        cv2.putText(imgBackground,str(studentInfo['major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)

        cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)

        cv2.putText(imgBackground,str(studentInfo['standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6,(100,100,100),
                    1)

        cv2.putText(imgBackground,str(studentInfo['starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)


        (w,h), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
        offset = (414-w)//2
        cv2.putText(imgBackground,str(studentInfo['name']),(808 + offset ,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)




    '''  
      imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
    counter+=1 
    '''
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)

import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancertdb-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancertdb.appspot.com"
})

# Get the absolute path to the 'images' folder
current_directory = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(current_directory, '..', 'images')

pathList = os.listdir(folderPath)
imgList = []
studentsIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentsIds.append(os.path.splitext(path)[0])

# Upload the images to the Firebase Storage bucket
bucket = storage.bucket()
for path in pathList:
    filePath = os.path.join(folderPath, path)
    blob = bucket.blob(f'images/{path}')
    blob.upload_from_filename(filePath)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        # Changing color from BGR:openCv to RGB:fcaeRecog
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print('Encoding Started ...')
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentsIds]
print('Encoding Complete')

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print('File Saved')

file = open("EncodeFile.p" , 'wb')
pickle.dump (encodeListKnownWithIds ,file)
file.close ()
print('File Saved')

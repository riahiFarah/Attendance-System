import cv2
import face_recognition
import pickle
import os

#importing the student images

# Get the absolute path to the 'images' folder
current_directory = os.path.dirname(os.path.abspath(__file__))
folderPath = os.path.join(current_directory, '..', 'images')


pathList = os.listdir(folderPath)
imgList = []

#print(pathList)
studentsIds = []
for path in pathList :
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    #print(path )
    #print(os.path.splitext(path)[0])
    studentsIds.append(os.path.splitext(path)[0])
print(studentsIds)


def findEncodings(imagesList) :
    encodeList = []
    for img in imagesList :
        #changing color from BGR:openCv to RGB:fcaeRecog
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


print('encoding Started ...')
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown , studentsIds]
#print(encodeListKnown)
print('Encoding Complete')

file = open("EncodeFile.p" , 'wb')
pickle.dump (encodeListKnownWithIds ,file)
file.close ()
print('File Saved')
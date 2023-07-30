import pickle
import cv2
import os

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

    imgBackground[162:162 + 480, 55:55 + 640] = img

    # Check if imgModeList has at least one valid image before accessing it
    if len(imgModeList) > 0:
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)

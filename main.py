import os
import pickle
import cv2
import face_recognition
import numpy as np
#import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facetrack-80ed9-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "facetrack-80ed9.appspot.com"
})

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Dodavanje slika iz patha
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imageModeList = []
for path in modePathList:
    img = cv2.imread(os.path.join(folderModePath, path))
    if img is None:
        print(f"Error loading image: {path}")
    else:
        imageModeList.append(img)

#ucitavanje
print("Ucitavanje enkodiranog fajla")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Fajl ucitan")

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imageModeList[0]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            print("Known face detected")
            print(f"Student ID: {studentIds[matchIndex]}")

            y1, x2, y2, x1 = [coord * 4 for coord in faceLoc]
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1

            cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)

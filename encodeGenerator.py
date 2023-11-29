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
    'databaseURL': "https://facetrack-80ed9-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "facetrack-80ed9.appspot.com"
})

#Importovanje svih slika studenata
folderPath = 'Images'
pathList = os.listdir(folderPath)
#print(pathList)
imageList = []
studentIds = []

for path in pathList:
    imageList.append(cv2.imread(os.path.join(folderPath, path)))
    #print(os.path.splitext(path)[0])
    studentIds.append(os.path.splitext(path)[0])

    #slanje slika u bazu
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
#print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for image in imagesList:
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodeList.append(encode)
    return encodeList

print("Pokrecemo enkodiranje...")
encodeListKnown = findEncodings(imageList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
#print(encodeListKnownWithIds)
print("Enkodiranje zavrseno")

#cuvanje fajlova
file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("Podaci su sacuvani")
import os
import face_recognition
from os import path

ROOT_FOLDER = '/mnt/iris1/Share/_daten/Fotos_Pressestelle_UK/'
ENCODED_FOLDER = ROOT_FOLDER + '_Professoren_Rektoren'

EXTENSIONS = ['.jpg', '.png', '.gif', '.bmp']

countFiles = 0

sourceImage = face_recognition.load_image_file(ENCODED_FOLDER + '/knoche.jpg')
sourceFace = face_recognition.face_encodings(sourceImage)[0]

results = []

print('start iterating images')
for root, dirs, files in os.walk(ROOT_FOLDER):
    #print(root)
    #print(files)

    for file in files:
        if any(file.endswith(ext) for ext in EXTENSIONS):
            filePath = path.join(root, file)
            print(filePath)
            unknownImage = face_recognition.load_image_file(filePath)
            unknownFaces = face_recognition.face_encodings(unknownImage)

            # Now we can see the two face encodings are of the same person with `compare_faces`!
            if unknownFaces:
                result = face_recognition.compare_faces([sourceFace], unknownFaces[0])

                if result[0] == True:
                    print('################################ Found face')
                    results.append(filePath)

    countFiles += len(files)
    #print('----------------------------------------')


print('countFiles: ' + str(countFiles))
print(results)
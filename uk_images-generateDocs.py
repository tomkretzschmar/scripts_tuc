import os
import json
from os import path
from os import listdir
from shutil import copyfile

SOURCE_FOLDER = 'D:/uk_img/orig_doc'
TARGET_FOLDER = 'D:/uk_img/doc/'

countFiles = 0

def getPersonScore(keypoints):
    score = 0.0
    for i in range(len(keypoints)//3):
        score += keypoints[i * 3 + 2]
    
    score = score/(len(keypoints)/3.0)             
    return score  

def doc_objects(filePath, fileBase, fileType):
    objects = []
    coordinates = []
    with open(filePath, 'r') as json_file:
        scoreMin = 0.275 #pauschal gesetzt
        json_data = json.load(json_file)
     
        for entry in json_data:
            if('framenr' in entry):
                continue
            elif(entry['confidence'] > scoreMin):
               objects.append(entry['elementtyp'])
               coordinates.append(entry['elementposition'])
        
    if(len(objects) > 0):
        target = {
            "reference": fileBase + fileType,
            "source": "yolov3",
            "type": "objects",
            "raw": "",
            "objects": objects,
            "objects_coordinates": coordinates
        }

        targetFile = TARGET_FOLDER + fileBase + '_objects' + fileType + '.json'

        print('___dump ' + targetFile)
        with open(targetFile, 'w') as outfile:
            json.dump(target, outfile, indent = 4)




def doc_persons(filePath, fileBase, fileType):
    personCount = 0
    with open(filePath, 'r') as json_file:
        scoreMin = 0.275 #pauschal gesetzt

        # OpenPose jsonVersion == '1.1'
        json_people = 'people'
        json_pose_keypoints = 'pose_keypoints'
        
        json_data = json.load(json_file)
        
        jsonVersion = json_data['version']
        
        if jsonVersion == 1.2:
            # OpenPose 1.4.0 jsonVersion == '1.2'
            json_people = 'people'
            json_pose_keypoints = 'pose_keypoints_2d'
            
        people = json_data[json_people]
        for person in people:
            keypoints = person[json_pose_keypoints]
            
            score = getPersonScore(keypoints)

            if score >= scoreMin:
                personCount += 1

        target = {
            "reference": fileBase + fileType,
            "source": "openpose",
            "type": "persons",
            "raw": "",
            "persons": personCount
        }
    targetFile = TARGET_FOLDER + fileBase + '_persons' + fileType + '.json'

    print('___dump ' + targetFile)
    with open(targetFile, 'w') as outfile:
        json.dump(target, outfile, indent = 4)


print('start iterating docs')
for root, dirs, files in os.walk(SOURCE_FOLDER):
    for file in files:
        if file.endswith('.json'):
            filePath = path.join(root, file)
            
            fileBase = file[:(file.rfind('_'))]
            if('keypoints' in file):
                #print('keypoints -> ' + filePath)
                doc_persons(filePath, fileBase, '.jpg')
            elif('yolov3' in file):
                #print('yolo -> ' + filePath)
                doc_objects(filePath, fileBase, '.jpg')


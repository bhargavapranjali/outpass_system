import time
import cv2
import os
import numpy as np
import json
from flask import current_app
import Project

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(img):
    
    face, rect = detect_face(img)

    filename = os.path.join(current_app.root_path, 'ML_model.json')
    test_file = open(filename,'r')
    data = json.load(test_file)
    val=False
    if face is not None:
        label, confidence = Project.recognition.predict(face)
        if (confidence<=80):
            print ('The confidence is: %s' % confidence)
            print(label)
            label_text = data["subjects"][label]
            print ('Welcome %s' % label_text)
            draw_rectangle(img, rect)
            draw_text(img, label_text, rect[0], rect[1]-5)
            cv2.imshow("Frame", img)
            val=True
            # time.sleep(1)
            return [img,val,label_text]
        else:
            draw_rectangle(img, rect)
            print ('The confidence is: %s' % confidence)
            cv2.imshow("Frame", img)
        
            return [img,val,None]
            
    else:
        return [img,val,None]

def predict_final():
    cap = cv2.VideoCapture(0)

    if Project.recognition is None:
        file_path = os.path.join(current_app.root_path, 'ML_model.json')
        test_file = open(file_path,'r')
        data = json.load(test_file)
        if len(data["labels"])==0:
            return None
        list_arrays = data["faces"]
        list1=[]
        for array in list_arrays:
            array = np.array(array, dtype=np.uint8)
            list1.append(array)

        test_file.close()
        Project.recognition = cv2.face.LBPHFaceRecognizer_create()
        Project.recognition.train(list1, np.array(data["labels"]))

    while True:
        ret,image = cap.read()
        list1 = predict(image)
        if list1[1]==True :
            cap.release()
            cv2.destroyAllWindows()
            return list1[2]

    cap.release()
    cv2.destroyAllWindows()

import secrets
import os
import time
import cv2
import numpy as np
import json
from Project import app
from json import JSONEncoder
from PIL import Image
from flask import current_app

def save_picture(form_picture, index):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if index==1:
        picture_path = os.path.join(current_app.root_path, 'static/photos', picture_fn)
    else:
        picture_path = os.path.join(current_app.root_path, 'static/signatures', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

def numpy_to_json(array):
    return array.tolist()

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]

def get_dataset(path_name):
    i=1
    time.sleep(1)
    cap = cv2.VideoCapture(0) 

    while i<21:
        if (i<21):
            ret,image = cap.read()
            face, rect = detect_face(image)
            
            if ret and face is not None:
                cv2.imshow("Frame", face)
                path = os.path.join(path_name,'%i.png')
                cv2.imwrite(path % i, face)
                print("Clicking %i image!" % i)
                i=i+1
                time.sleep(0.1)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if (i>=21):
            cap.release()
            cv2.destroyAllWindows()

def prepare_training_data(data_folder_path,name):

    face1 = []
    label1 = []
    file_path = os.path.join(app.root_path,'static/recognition')
    files = os.listdir(file_path) 
    label = int(len(files))
    subject_images_names = os.listdir(data_folder_path)
    for image_name in subject_images_names:
        
        image_path = os.path.join(data_folder_path,image_name)

        image = cv2.imread(image_path)

        cv2.imshow("Training on image...", image)
        cv2.waitKey(100)
        
        face, rect = detect_face(image)
        
        if face is not None:
            face1.append(face)
            label1.append(label) 
    
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    file_name = os.path.join(app.root_path, 'ML_model.json')
    test_file = open(file_name,'r')
    data = json.load(test_file)
    test_file.close()

    numpy_faces = data["faces"]
    numpy_labels = data["labels"]
    numpy_subjects = data["subjects"]

    for face in face1:
        json_array = numpy_to_json(face)
        numpy_faces.append(json_array)

    for label in label1:
        numpy_labels.append(label)

    numpy_subjects.append(name)
    
    
    test_file = open(file_name, "w") 
    numpy_data = {"faces" : numpy_faces, "labels": numpy_labels, "subjects":numpy_subjects}
    test_file.write(json.dumps(numpy_data))
    test_file.close()




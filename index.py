from ast import Not
from multiprocessing import connection
from pickle import FALSE
from requests import session
import streamlit as st
import face_recognition
import numpy as np
from PIL import Image, ImageDraw
from IPython.display import display
import cv2
import csv
import os
from PIL import Image, ImageDraw
from IPython.display import display
from datetime import datetime
import mysql.connector
import ctypes




# Load a second sample picture and learn how to recognize it.
rohan_image = face_recognition.load_image_file("Students/rohan.jpg")
rohan_face_encoding = face_recognition.face_encodings(rohan_image)[0]   

# Load a second sample picture and learn how to recognize it.
raghu_image = face_recognition.load_image_file("Students/raghu.png")
raghu_face_encoding = face_recognition.face_encodings(raghu_image)[0]

adarsh_image = face_recognition.load_image_file("Students/adarsh.png")
adarsh_face_encoding = face_recognition.face_encodings(adarsh_image)[0]




# Create arrays of known face encodings and their names
known_face_encodings = [
    rohan_face_encoding,
    raghu_face_encoding,
]
known_face_names = [
  
    "Rohan Padhye",
    "Raghuttam Parvatikar",
    
]


# Initialize some variables





# nav = st.sidebar.radio("Navigation", ["Attendance", "Management System", "About Us"])

# cnx = mysql.connector.connect(user='root', password='123!@QWE',
#                               host='127.0.0.1',
#                               database='ATTENDANCE_SYSTEM')


att=[]

def markAttendance(name):
    with open('cache.csv','+r') as f:
        myDataList= f.readlines()
        nameList=[]
        for lines in myDataList: 
            entry=lines.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            f.writelines(f'\n{name}')
           
        
st.session_state
st.session_state['names']= []
st.title("Attendance")

def runVideo():
    try: 
        os.remove('cache.csv')
    except: 
        print("err")
    with open('cache.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    run = st.checkbox('Run',value=True) 
    FRAME_WINDOW = st.image([]) 
    cam = cv2.VideoCapture(0)
    aList=[]
    while run:
        ret, frame = cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"


                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    # markAttendance(name)
                    if name not in st.session_state['names']:
                         st.session_state['names'].append(name)
                
                
                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        FRAME_WINDOW.image(frame)      
    return aList



newV = runVideo()
# with open('cache.csv','+r') as f:
#     myDataList= f.readlines()
#     print(myDataList)
#     print('here')




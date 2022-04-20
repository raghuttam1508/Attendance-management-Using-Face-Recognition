from multiprocessing import connection
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






# Load a second sample picture and learn how to recognize it.
rohan_image = face_recognition.load_image_file("Students/rohan.jpg")
rohan_face_encoding = face_recognition.face_encodings(rohan_image)[0]

# Load a second sample picture and learn how to recognize it.
raghu_image = face_recognition.load_image_file("Students/raghu.png")
raghu_face_encoding = face_recognition.face_encodings(raghu_image)[0]


# Load a second sample picture and learn how to recognize it.
omkar_image = face_recognition.load_image_file("Students/omkar2.jpeg")
omkar_face_encoding = face_recognition.face_encodings(omkar_image)[0]

# Load a second sample picture and learn how to recognize it.
adarsh_image = face_recognition.load_image_file("Students/adarsh.png")
adarsh_face_encoding = face_recognition.face_encodings(adarsh_image)[0]

# Load a second sample picture and learn how to recognize it.
vishnu_image = face_recognition.load_image_file("Students/vishnu.png")
vishnu_face_encoding = face_recognition.face_encodings(vishnu_image)[0]


known_face_encodings = [
  
    rohan_face_encoding,
    raghu_face_encoding,
    omkar_face_encoding,
    adarsh_face_encoding,
    vishnu_face_encoding,


    
]
known_face_names = [
  
    "Rohan Padhye",
    "Raghuttam Parvatikar",
    "Omkar Pawar",
    "Adarsh Kadam",
    "Vishnu",

]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True



nav = st.sidebar.radio("Navigation", ["Attendance", "Management System", "About Us"])

cnx = mysql.connector.connect(user='root', password='123!@QWE',
                              host='127.0.0.1',
                              database='ATTENDANCE_SYSTEM')

present_students=['Hey']

def markAttendance(name):  
    if name not in present_students:
        present_students.append(name)
if nav == "Attendance":
    st.title("Attendance")
    run = st.checkbox('Run',value=True)
    FRAME_WINDOW = st.image([]) 
    cam = cv2.VideoCapture(0)
    #creating a list for Storing present students list

    
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

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    
                
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

        # Display the resulting image


        # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        FRAME_WINDOW.image(frame)
        if name not in present_students:
            present_students.append(name)
        markAttendance(name)
        present_students.append(name)

        
    else:
        
        st.write('Stopped')

    # try:
    #     connection = mysql.connector.connect(
    #         host="localhost", database="Attendance", user="root", password="root",
    #     )

    #     if connection.isConnected():
    #         info = connection.get_server_info()
    #         st.write("CONNECTED!")
    #         cursor = connection.cursor()
    #         cursor.execute("select database();")
    #         record = cursor.fetchone()
    #         st.write("You're connected to database: ", record)

    # except Error as e:
    #     st.write("Error while connecting to MySQL", e)


if nav == "Management System":
    st.title("Management System")


if nav == "About Us":
    st.title("About Us")

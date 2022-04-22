from fileinput import filename
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
import ctypes


# Load a second sample picture and learn how to recognize it.
rohan_image = face_recognition.load_image_file("Students/rohan.jpg")
rohan_face_encoding = face_recognition.face_encodings(rohan_image)[0]


raghu_image = face_recognition.load_image_file("Students/raghu.png")
raghu_face_encoding = face_recognition.face_encodings(raghu_image)[0]



omkar_image = face_recognition.load_image_file("Students/omkar2.jpeg")
omkar_face_encoding = face_recognition.face_encodings(omkar_image)[0]


adarsh_image = face_recognition.load_image_file("Students/adarsh.png")
adarsh_face_encoding = face_recognition.face_encodings(adarsh_image)[0]


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




nav = st.sidebar.radio("Navigation", ["Attendance", "Management System", "About Us"])



att=[]
header = ['Name', 'Time']
now=datetime.now()
fileName = now.strftime('%H:%M:%S')
with open(fileName+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)




def markAttendance(name):    
    global fileName
    with open(fileName+'.csv','+r') as f:
        myDataList= f.readlines()
        nameList=[]
        for lines in myDataList: 
            entry=lines.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            att.append(name)




def startVideo():
    
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123!@QWE",
        database="ATTENDANCE_SYSTEM" 
    )

    now = datetime.now()
    today = datetime.today()

    # dd/mm/YY
    Date = today.strftime("%d/%m/%Y")
    Time= now.strftime("%H:%M:%S")
    mycursor = mydb.cursor()
 
    mycursor.execute("SELECT * FROM AI_DS;")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    
    
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    run = st.checkbox('Run',value=True)
    FRAME_WINDOW = st.image([]) 
    cam = cv2.VideoCapture(0)
    att=[]
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
                    if name not in att:
                        att.append(name)
                        markAttendance(name)
                        mycursor.execute('INSERT INTO AI_DS VALUES ("' +name+ '","' +Date+ '","'+ Time+'");')
                        mydb.commit()
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
    else:
        mydb.close()
        st.write('Stopped')
        text_contents = '''CSV CONTENT'''
        st.download_button('Download CSV', text_contents)
if nav == "Attendance":
    st.title("Attendance")
    startVideo()
    

if nav == "Management System":
    st.title("Management System")


if nav == "About Us":
    st.title("About Us")
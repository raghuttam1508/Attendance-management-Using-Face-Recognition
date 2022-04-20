from multiprocessing import connection
import streamlit as st
import mysql.connector
from mysql.connector import Error

from streamlit_webrtc import webrtc_streamer


nav = st.sidebar.radio("Navigation", ["Attendance", "Management System", "About Us"])

if nav == "Attendance":
    st.title("Attendance")
    webrtc_streamer(key="sample")

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

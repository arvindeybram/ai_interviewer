import mysql.connector
from mysql.connector import Error
import streamlit as st

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="leetcode_db"
        )
        return connection
    except Error as e:
        st.error(f"❌ MySQL connection error: {e}")
        return None

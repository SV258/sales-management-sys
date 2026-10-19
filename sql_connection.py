
import mysql.connector
import streamlit as st

def get_sql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="sql_reporter",
        password=st.secrets["sql_reporter_password"],
        database="sales_management_sys"
    )

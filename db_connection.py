import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Ilovechocolateof03",
        database="LearningProductivityDB"
    )
    return conn

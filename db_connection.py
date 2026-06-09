import mysql.connector

def getConnection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Ilovechocolateof03",
        database="LearningProductivityDB"
    )
    return conn

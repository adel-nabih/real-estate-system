import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="A2d3e5l7",
        database="real_estate_db",
    )
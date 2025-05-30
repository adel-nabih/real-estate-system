# just testing the connection to the database
# all good :) its working
from config.db_config import get_connection

def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Connected successfully. Tables:")
        for table in tables:
            print("-", table[0])
        cursor.close()
        conn.close()
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    test_connection()

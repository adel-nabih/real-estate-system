from config.db_config import get_connection

def execute_query(query, values=None, fetch=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, values)
        if fetch:
            return cursor.fetchall()
        conn.commit()
    finally:
        cursor.close()
        conn.close()

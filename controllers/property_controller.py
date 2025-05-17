from utils.db_helper import execute_query
from models.property import Property
from config.db_config import get_connection

def add_property(property_obj):
    query = """
        INSERT INTO properties (location, type, size, price, status, broker_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (
        property_obj.location,
        property_obj.type,
        property_obj.size,
        property_obj.price,
        property_obj.status,
        property_obj.broker_id
    )
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    property_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return property_id

def get_all_properties():
    query = "SELECT * FROM properties"
    rows = execute_query(query, fetch=True)
    return [Property.from_dict(row) for row in rows]

def assign_broker_to_property(property_id, broker_id):
    query = "UPDATE properties SET broker_id = %s WHERE id = %s"
    values = (broker_id, property_id)
    execute_query(query, values)

from utils.db_helper import execute_query
from models.property import Property
from config.db_config import get_connection

def add_property(property_obj: Property): # Renamed 'property' to 'property_obj' to avoid keyword conflict
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

def get_property_by_id(property_id):
    query = """
        SELECT p.*, b.name as broker_name 
        FROM properties p 
        LEFT JOIN brokers b ON p.broker_id = b.id 
        WHERE p.id = %s
    """
    # FIX: Removed fetch_one=True. execute_query with fetch=True returns a list of rows.
    rows = execute_query(query, (property_id,), fetch=True)
    # Return the first row if the list is not empty, otherwise None.
    return Property.from_dict(rows[0]) if rows else None

def update_property(property_obj: Property): # Renamed 'property' to 'property_obj'
    query = """
        UPDATE properties 
        SET location = %s, type = %s, size = %s, price = %s, status = %s, broker_id = %s
        WHERE id = %s
    """
    values = (
        property_obj.location,
        property_obj.type,
        property_obj.size,
        property_obj.price,
        property_obj.status,
        property_obj.broker_id,
        property_obj.id
    )
    execute_query(query, values)
    return True

def delete_property(property_id):
    query = "DELETE FROM properties WHERE id = %s"
    execute_query(query, (property_id,))
    return True

def get_available_properties():
    query = """
        SELECT p.*, b.name as broker_name 
        FROM properties p 
        LEFT JOIN brokers b ON p.broker_id = b.id 
        WHERE p.status = 'available'
    """
    rows = execute_query(query, fetch=True)
    return [Property.from_dict(row) for row in rows]

def get_property_sales(property_id):
    query = """
        SELECT s.*, 
               p.location as property_location,
               c.name as client_name,
               b.name as broker_name
        FROM sales s
        JOIN properties p ON s.property_id = p.id
        JOIN clients c ON s.client_id = c.id
        JOIN brokers b ON s.broker_id = b.id
        WHERE s.property_id = %s
    """
    rows = execute_query(query, (property_id,), fetch=True)
    return rows

from utils.db_helper import execute_query
from models.client import Client

def add_client(client: Client):
    query = """
        INSERT INTO clients (name, contact, preferences, broker_id)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        client.name,
        client.contact,
        client.preferences,
        client.broker_id
    )
    execute_query(query, values)

def get_all_clients():
    query = "SELECT * FROM clients"
    rows = execute_query(query, fetch=True)
    return [Client.from_dict(row) for row in rows]

def assign_broker_to_client(client_id, broker_id):
    query = "UPDATE clients SET broker_id = %s WHERE id = %s"
    values = (broker_id, client_id)
    execute_query(query, values)

def get_client_by_id(client_id):
    query = """
        SELECT c.*, b.name as broker_name 
        FROM clients c 
        LEFT JOIN brokers b ON c.broker_id = b.id 
        WHERE c.id = %s
    """
    row = execute_query(query, (client_id,), fetch=True, fetch_one=True)
    return Client.from_dict(row) if row else None

def update_client(client: Client):
    query = """
        UPDATE clients 
        SET name = %s, contact = %s, preferences = %s, broker_id = %s
        WHERE id = %s
    """
    values = (
        client.name,
        client.contact,
        client.preferences,
        client.broker_id,
        client.id
    )
    execute_query(query, values)
    return True

def delete_client(client_id):
    query = "DELETE FROM clients WHERE id = %s"
    execute_query(query, (client_id,))
    return True

def get_client_sales(client_id):
    query = """
        SELECT s.*, 
               p.location as property_location,
               c.name as client_name,
               b.name as broker_name
        FROM sales s
        JOIN properties p ON s.property_id = p.id
        JOIN clients c ON s.client_id = c.id
        JOIN brokers b ON s.broker_id = b.id
        WHERE s.client_id = %s
    """
    rows = execute_query(query, (client_id,), fetch=True)
    return rows

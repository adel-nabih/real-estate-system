from utils.db_helper import execute_query
from models.client import Client

def add_client(client_obj):
    query = """
        INSERT INTO clients (name, contact, preferences, broker_id)
        VALUES (%s, %s, %s, %s)
    """
    values = (
        client_obj.name,
        client_obj.contact,
        client_obj.preferences,
        client_obj.broker_id
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

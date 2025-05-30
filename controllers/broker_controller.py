from utils.db_helper import execute_query
from models.broker import Broker

def add_broker(broker: Broker):
    query = """
        INSERT INTO brokers (name, years_experience)
        VALUES (%s, %s)
    """
    values = (broker.name, broker.years_experience)
    execute_query(query, values)

def get_all_brokers():
    query = "SELECT * FROM brokers"
    rows = execute_query(query, fetch=True)
    return [Broker.from_dict(row) for row in rows]

def get_broker_by_id(broker_id):
    query = "SELECT * FROM brokers WHERE id = %s"
    rows = execute_query(query, (broker_id,), fetch=True)
    return Broker.from_dict(rows[0]) if rows else None

def update_broker(broker: Broker):
    query = """
        UPDATE brokers 
        SET name = %s, years_experience = %s
        WHERE id = %s
    """
    values = (broker.name, broker.years_experience, broker.id)
    execute_query(query, values)
    return True

def delete_broker(broker_id):
    query = "DELETE FROM brokers WHERE id = %s"
    execute_query(query, (broker_id,))
    return True

def get_broker_sales(broker_id):
    query = """
        SELECT s.*, 
               p.location as property_location,
               c.name as client_name,
               b.name as broker_name
        FROM sales s
        JOIN properties p ON s.property_id = p.id
        JOIN clients c ON s.client_id = c.id
        JOIN brokers b ON s.broker_id = b.id
        WHERE s.broker_id = %s
    """
    rows = execute_query(query, (broker_id,), fetch=True)
    return rows

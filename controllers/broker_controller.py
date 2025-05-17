from utils.db_helper import execute_query
from models.broker import Broker

def add_broker(broker_obj):
    query = """
        INSERT INTO brokers (name, years_experience)
        VALUES (%s, %s)
    """
    values = (broker_obj.name, broker_obj.years_experience)
    execute_query(query, values)

def get_all_brokers():
    query = "SELECT * FROM brokers"
    rows = execute_query(query, fetch=True)
    return [Broker.from_dict(row) for row in rows]

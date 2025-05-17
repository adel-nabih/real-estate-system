from utils.db_helper import execute_query
from config.db_config import get_connection
from models.sale import Sale

def add_sale(sale_obj):
    # Insert sale record
    query = """
        INSERT INTO sales (property_id, client_id, broker_id, date, final_price)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        sale_obj.property_id,
        sale_obj.client_id,
        sale_obj.broker_id,
        sale_obj.date,
        sale_obj.final_price
    )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    sale_id = cursor.lastrowid

    # Update property status to "sold"
    update_query = "UPDATE properties SET status = 'sold' WHERE id = %s"
    cursor.execute(update_query, (sale_obj.property_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return sale_id

def get_all_sales():
    query = "SELECT * FROM sales"
    rows = execute_query(query, fetch=True)
    return [Sale.from_dict(row) for row in rows]

from utils.db_helper import execute_query
from config.db_config import get_connection
from models.sale import Sale

def add_sale(sale: Sale):
    # Insert sale record
    query = """
        INSERT INTO sales (property_id, client_id, broker_id, date, final_price)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        sale.property_id,
        sale.client_id,
        sale.broker_id,
        sale.date,
        sale.final_price
    )

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    sale_id = cursor.lastrowid

    # Update property status to "sold"
    update_query = "UPDATE properties SET status = 'sold' WHERE id = %s"
    cursor.execute(update_query, (sale.property_id,))
    conn.commit()

    cursor.close()
    conn.close()
    return sale_id

def get_all_sales():
    query = "SELECT * FROM sales"
    rows = execute_query(query, fetch=True)
    return [Sale.from_dict(row) for row in rows]

def get_sale_by_id(sale_id):
    query = """
        SELECT s.*, 
               p.location as property_location,
               c.name as client_name,
               b.name as broker_name
        FROM sales s
        JOIN properties p ON s.property_id = p.id
        JOIN clients c ON s.client_id = c.id
        JOIN brokers b ON s.broker_id = b.id
        WHERE s.id = %s
    """
    row = execute_query(query, (sale_id,), fetch=True, fetch_one=True)
    return Sale.from_dict(row) if row else None

def update_sale(sale: Sale):
    query = """
        UPDATE sales 
        SET property_id = %s, client_id = %s, broker_id = %s, date = %s, final_price = %s
        WHERE id = %s
    """
    values = (
        sale.property_id,
        sale.client_id,
        sale.broker_id,
        sale.date,
        sale.final_price,
        sale.id
    )
    execute_query(query, values)
    return True

def delete_sale(sale_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get the property_id before deleting the sale
        get_property_query = "SELECT property_id FROM sales WHERE id = %s"
        cursor.execute(get_property_query, (sale_id,))
        result = cursor.fetchone()
        
        if result:
            property_id = result[0]
            # Update property status back to available
            update_property_query = "UPDATE properties SET status = 'available' WHERE id = %s"
            cursor.execute(update_property_query, (property_id,))
        
        # Delete the sale
        delete_query = "DELETE FROM sales WHERE id = %s"
        cursor.execute(delete_query, (sale_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting sale: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_sales_by_date_range(start_date, end_date):
    query = """
        SELECT s.*, 
               p.location as property_location,
               c.name as client_name,
               b.name as broker_name
        FROM sales s
        JOIN properties p ON s.property_id = p.id
        JOIN clients c ON s.client_id = c.id
        JOIN brokers b ON s.broker_id = b.id
        WHERE s.date BETWEEN %s AND %s
    """
    rows = execute_query(query, (start_date, end_date), fetch=True)
    return [Sale.from_dict(row) for row in rows]

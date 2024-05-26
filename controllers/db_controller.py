import psycopg2
from db.config import load_config

def create_order(description: str, amount: str, user_id: int = None):
    config = load_config()
    sql = "insert into orders(description, amount, user_id) values (%s, %s, %s) returning id"
    if user_id == None:
        sql = "insert into orders(description, amount) values (%s, %s) returning id"
    
    try:
        print(user_id)
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (description, amount) if user_id == None else (description, amount, user_id))           
                rows = cur.fetchone()
                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        conn.close()
        return rows[0]
    
def delete_order(id):
    config = load_config()
    sql = f"delete from orders where id = '{id}'"
    
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql)                       
                conn.commit()
                return 'delete is successful'
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        conn.close()

def get_orders():
    config = load_config()
    sql = "select * from orders"
    
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)           
                orders = cur.fetchall()
                return orders
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        conn.close()

def get_order(id):
    config = load_config()
    sql = f"select * from orders where id = '{id}'"
    
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)           
                order = cur.fetchone()
                return order
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        conn.close()

if __name__ == '__main__':
    create_order()
import psycopg
from fastapi.encoders import jsonable_encoder

from configs.db import DB_DATA
from models.order import Order


def create_order(description: str, amount: int, user_id: int = None):
    sql = "insert into orders(description, amount, user_id) values (%s, %s, %s) returning id"
    if user_id is None:
        sql = "insert into orders(description, amount) values (%s, %s) returning id"

    conn = psycopg.connect(DB_DATA)
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (description, amount) if user_id is None else (description, amount, user_id))
            order_id = cur.fetchone()

            conn.commit()
            cur.execute(f"select * from orders where id = '{order_id[0]}'")
            order_info = cur.fetchone()

            return jsonable_encoder(Order(id=str(order_info[0]), description=order_info[1], amount=order_info[2],
                                          user_id=order_info[3]))
    except Exception as error:
        conn.rollback()
        print(error)
        raise error
    finally:
        conn.close()


def delete_order(id):
    sql = f"delete from orders where id = '{id}'"

    conn = psycopg.connect(DB_DATA)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
            return
    except (Exception, psycopg.DatabaseError) as error:
        conn.rollback()
        print(error)
        raise {'status': 'failed', 'message': error}
    finally:
        conn.close()


def get_orders():
    sql = "select * from orders"

    conn = psycopg.connect(DB_DATA)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            orders = cur.fetchall()
            # todo(): check result in orders
            result_orders = []

            for order in orders:
                result_orders.append(
                    Order(id=str(order[0]), description=order[1], amount=order[2], user_id=order[3]))

            return result_orders
    except (Exception, psycopg.DatabaseError) as error:
        conn.rollback()
        print(error)
    finally:
        conn.close()


def get_order(order_id):
    sql = f"select * from orders where id = '{order_id}'"

    conn = psycopg.connect(DB_DATA)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            order_info = cur.fetchone()
            if order_info is None: raise Exception(f"order by id {order_id} not found")

            return Order(id=str(order_info[0]), description=order_info[1], amount=order_info[2], user_id=order_info[3])
    except (Exception, psycopg.DatabaseError) as error:
        conn.rollback()
        raise NameError(error)
    finally:
        conn.close()


if __name__ == '__main__':
    create_order()
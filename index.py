from flask import request, jsonify, Response
from flask import Flask, json
import statsd
import calendar;
import time;
from controllers.db_controller import create_order, get_order, get_orders, delete_order


api = Flask(__name__)
ordersGraphiteClient = statsd.StatsClient('147.45.41.137', 8125, prefix='orders')
timingGraphiteClient = statsd.StatsClient('147.45.41.137', 8125)

@api.post('/orders/create')
def request_create_orders():
    try:
        time_start = round(time.time() * 1000)
        print(time_start)
        data = request.json
        if (data['description'] == None or data['amount'] == None or data['user_id'] == None): raise ValueError            
        result = create_order(data['description'], data['amount'], data['user_id'])
        ordersGraphiteClient.set("create.succeeded", 1)
        timingGraphiteClient.timing("orders.create", round(time.time() * 1000) - time_start)
        return jsonify(status="succeeded", id=result)
    except ValueError as e:
        ordersGraphiteClient.set('create.failed', 1)
        return jsonify(
            status='failed',
            message='Missing description or amount in request'
        )
    except Exception as e:
        ordersGraphiteClient.set('create.failed', 1)
        timingGraphiteClient.timing("orders.create", round(time.time() * 1000) - time_start)
        return jsonify(status='error', exception=str(e)), 400

@api.get('/order')
def request_get_order():
    try:
        time_start = round(time.time() * 1000)
        id = request.args.get('id')
        result = get_order(id)

        ordersGraphiteClient.set('get_one.succeeded', 1)
        timingGraphiteClient.timing("orders.get_one", round(time.time() * 1000) - time_start)
        return jsonify(
            status="succeeded",
            result=result
        )
    except Exception as e:
        ordersGraphiteClient.set('get_one.failed', 1)
        timingGraphiteClient.timing("orders.get_one", round(time.time() * 1000) - time_start)
        return jsonify(status='failed', exception=str(e))


@api.get('/orders')
def request_get_orders():
    try:
        time_start = round(time.time() * 1000)
        id = request.args.get('id')

        if (id):
            result = get_order(id)            
        else:
            result = get_orders()

        ordersGraphiteClient.set('get.succeeded', 1)
        timingGraphiteClient.timing("orders.get", round(time.time() * 1000) - time_start)
        return jsonify(
            status="succeeded",
            result=result
        )
    except Exception as e:
        ordersGraphiteClient.set('get.failed', 1)
        timingGraphiteClient.timing("orders.get", round(time.time() * 1000) - time_start)
        return jsonify(status='failed', exception=str(e))

@api.delete('/order')
def request_delete_order():
    try:
        time_start = round(time.time() * 1000)
        id = request.args.get('id')
        if id == None: raise Exception("ID in request is empty")

        result = delete_order(id)
        ordersGraphiteClient.set('delete.succeeded', 1)
        timingGraphiteClient.timing("orders.delete", round(time.time() * 1000) - time_start)
        return jsonify(
            status='succeeded',
            result=result
        ), 200
    except Exception as e:
        ordersGraphiteClient.set('delete.failed', 1)
        timingGraphiteClient.timing("orders.delete", round(time.time() * 1000) - time_start)
        return jsonify(status='failed', exception=str(e)), 400

if __name__ == '__main__':
    api.run()


# c.timing("stats.timed", 320)
# c.set("", 1)
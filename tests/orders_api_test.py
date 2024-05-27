import random

import requests
import json
import time

test_description = {
    'empty_string': '',  # empty string
    '245_symbols': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
    # 245 symbols
    '128_symbols': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy t.",
    # 128 symbols
    '129_symbols': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy te.",
    # 129 symbols
    '49_symbols': 'Lorem Ipsum is simply dummy text of the printing.'  # 49 symbols
}

test_amount = [
    0.99, 1, 15000, 350000, 350000.01, 540000
]

test_user_id = [
    0, 3, 6
    # first id of user = 1 (id 0 is undefined)
    # 6 = now count of users - 5 (max id 5)
]

test_data = [
    # result = заказ должен создаться
    {'description': test_description['49_symbols'], 'amount': test_amount[2], 'user_id': test_user_id[1], 'result': True},
    {'description': test_description['128_symbols'], 'amount': test_amount[1], 'user_id': test_user_id[1], 'result': True},
    {'description': test_description['49_symbols'], 'amount': test_amount[3], 'user_id': test_user_id[1], 'result': True},
    {'description': test_description['128_symbols'], 'amount': test_amount[4], 'user_id': test_user_id[1], 'result': True},
    {'description': test_description['129_symbols'], 'amount': test_amount[2], 'user_id': test_user_id[2], 'result': False},
    {'description': test_description['empty_string'], 'amount': test_amount[0], 'user_id': test_user_id[0], 'result': False},
    {'description': test_description['245_symbols'], 'amount': test_amount[2], 'user_id': test_user_id[0], 'result': False}
]


def create_order_test(data):
    url = "http://localhost:8000/orders/create"
    headers = {
        'Content-Type': 'application/json'
    }

    del data['result']

    payload = json.dumps(data)
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


def get_order_info(id):
    url = f"http://localhost:8000/orders/{id}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)

def get_orders():
    url = "http://localhost:8000/orders"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return json.loads(response.text)


def delete_order(id):
    url = f"http://localhost:8000/orders/{id}"
    headers = {
        'Content-Type': 'application/json'
    }
    requests.request("DELETE", url, headers=headers)


def checkEquivalenceClassesCreateOrder():
    # Позитивные и негативные проверки полей для создания заказа в API

    for case in test_data:
        time_start = round(time.time() * 1000)
        expected_result = case.get('result')
        json_response = create_order_test(case)

        def have_order_key():
            return True if 'order' in json_response.keys() else False

        result = (f'Test passed?: {expected_result == have_order_key()} | Expected result: {expected_result} | Actual '
                  f'result: {have_order_key()} | Response: {json_response} | Execution time: {round(time.time() * 1000) - time_start} ms')
        print(result)

def checkAllMethodsOrdersAPIStepByStep():
    # Проверка полного цикла заказа со всеми методами в API
    correct_data = test_data[0]

    create_order_result = create_order_test(correct_data)
    order_id = create_order_result.get('order').get('id')
    print(f'Step 1 | Create order | Actual result: {order_id is not None} | Response: {create_order_result}')

    get_order_result = get_order_info(order_id)
    print(f'Step 2 | Get order info by id | Create order response and get order response is the same: {create_order_result == get_order_result}')

    get_all_orders = get_orders()
    order_is_present_in_list = False
    for order in get_all_orders.get('orders'):
        new_order_id = order.get('id')
        if new_order_id == order_id: order_is_present_in_list = True

    print(f'Step 3 | Get all orders and check order by id in list | Order id found in list: {order_is_present_in_list}')

    delete_order_result = delete_order(order_id)
    order_is_deleted = delete_order_result.get('status') == 'succeeded'
    print(f'Step 4 | Delete order | API response is succeeded: {order_is_deleted}')

    check_order_after_delete = get_order_result(order_id)
    print(f"Step 5 | Get order by id after delete | Result: {check_order_after_delete}")


# checkEquivalenceClassesCreateOrder()
# checkAllMethodsOrdersAPI()

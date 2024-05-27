import statsd
import time
from fastapi.encoders import jsonable_encoder

from app import InvalidRequestException
from configs.limits import MAX_AMOUNT, MIN_AMOUNT
from controllers.db_controller_orders import create_order, delete_order, get_orders, get_order
from fastapi import HTTPException, status, APIRouter

from helpers.api_helper import get_uuid_str
from helpers.exceptions_helper import InternalServerException
from models.order import CreateOrder
from models.api_response import OrderResponse, ApiErrorResponse, ApiSuccessResponse, GetOrdersResponse

orders_router = APIRouter(tags=["/orders (order management)"])

ordersGraphiteClient = statsd.StatsClient('147.45.41.137', 8125, prefix='orders')
timingGraphiteClient = statsd.StatsClient('147.45.41.137', 8125)


@orders_router.post('/create',
                    responses={
                        201: {"model": OrderResponse, "description": "ok, rder successfully created"},
                        400: {"model": ApiErrorResponse, "description": "failed, usually the problem is passing incorrect parameters or exceeding the limit"},
                        500: {"model": ApiErrorResponse, "description": "unexpected error"}
                    })
def create_order_request(order: CreateOrder):
    time_start = round(time.time() * 1000)
    try:
        if 1 > len(order.description) or len(order.description) > 128: raise InvalidRequestException(
            "description must be from 1 to 128 characters")
        if MIN_AMOUNT >= order.amount or order.amount > MAX_AMOUNT: raise InvalidRequestException(
            f"amount must be more than {MIN_AMOUNT} ruble and less than {MAX_AMOUNT} rubles")
        if type(order.user_id) != int: raise InvalidRequestException("user_id must be in int format")

        result = create_order(order.description, order.amount, order.user_id)
        ordersGraphiteClient.set("create.succeeded", 1)
        return jsonable_encoder(OrderResponse(status="succeeded", order=result))
    except InvalidRequestException as e:
        ordersGraphiteClient.set('create.failed', 1)
        raise e
    except Exception as e:
        ordersGraphiteClient.set('create.error', 1)
        raise InternalServerException(str(e))
    finally:
        timingGraphiteClient.timing("orders.create", round(time.time() * 1000) - time_start)


@orders_router.get('/{order_id}',
                   responses={
                       200: {"model": OrderResponse, "description": "ok, the response must contain the status and information about the order"},
                       404: {"model": ApiErrorResponse, "description": "order_id is not found"},
                       500: {"model": ApiErrorResponse, "description": "unexpected error"}
                   },
                   description="Входной параметр = ID заказа. При корректном ID, который есть в БД, должна вернуться информация о нем в формате модели Order. Если ID не найдено в БД, вернуть ошибку (модель FailedOrderResponse).")
def request_get_order(order_id: str):
    time_start = round(time.time() * 1000)
    try:
        if get_uuid_str(order_id) is None: raise InvalidRequestException(name="order id must be UUIDv4 format")
        result = get_order(order_id)
        ordersGraphiteClient.set('get_one.succeeded', 1)
        return jsonable_encoder(OrderResponse(status="succeeded", order=result))
    except InvalidRequestException as e:
        ordersGraphiteClient.set('get_one.failed', 1)
        raise e
    except NameError as e:
        ordersGraphiteClient.set('get_one.failed', 1)
        raise InvalidRequestException(str(e))
    except Exception:
        ordersGraphiteClient.set('get_one.error', 1)
        raise InternalServerException(name="an error occurred on the server side")
    finally:
        timingGraphiteClient.timing("orders.get_one", round(time.time() * 1000) - time_start)


@orders_router.get('',
                   responses={
                        200: {"model": GetOrdersResponse},
                        500: {"model": ApiErrorResponse},
                   })
def request_get_orders():
    time_start = round(time.time() * 1000)
    try:
        # todo(): сделать ограничение по выдаче, тк записей может быть довольно много
        result = get_orders()
        ordersGraphiteClient.set('get.succeeded', 1)
        return jsonable_encoder(GetOrdersResponse(status="succeeded", orders=result))
    except Exception:
        ordersGraphiteClient.set('get.failed', 1)
        raise InternalServerException(name="an error occurred on the server side")
    finally:
        timingGraphiteClient.timing("orders.get", round(time.time() * 1000) - time_start)


@orders_router.delete('/{order_id}',
                      responses={
                          200: {"model": ApiSuccessResponse},
                          400: {"model": ApiErrorResponse},
                          500: {"model": ApiErrorResponse}
                      })
def request_delete_order(order_id: str):
    time_start = round(time.time() * 1000)
    try:
        if id is None: raise InvalidRequestException(name="ID in request is empty")
        delete_order(order_id)

        ordersGraphiteClient.set('delete.succeeded', 1)
        return jsonable_encoder(
            ApiSuccessResponse(status="succeeded", message=f'order_id: {order_id} was deleted is sucessful'))
    except InvalidRequestException as e:
        raise e
    except Exception as e:
        print(e)
        ordersGraphiteClient.set('delete.failed', 1)
        raise InternalServerException(name="an error occurred on the server side")
    finally:
        timingGraphiteClient.timing("orders.delete", round(time.time() * 1000) - time_start)

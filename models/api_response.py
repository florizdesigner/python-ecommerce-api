from pydantic import BaseModel, UUID4
from models.order import Order


class OrderResponse(BaseModel):
    status: str
    order: Order


class FailedOrderResponse(BaseModel):
    status: str
    message: str


class GetOrdersResponse(BaseModel):
    status: str
    orders: list[Order]


class ApiSuccessResponse(BaseModel):
    status: str
    message: str


class ApiErrorResponse(BaseModel):
    status: str
    message: str

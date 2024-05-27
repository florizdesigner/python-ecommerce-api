from urllib.request import Request

from starlette.responses import JSONResponse
from fastapi import FastAPI

from helpers.exceptions_helper import InvalidRequestException, InternalServerException
from routes.orders_route import orders_router


def build_app() -> FastAPI:
    app = FastAPI(
        title="Ecommerce API",
        version="0.0.1"
    )

    @app.exception_handler(InvalidRequestException)
    def invalid_request_exception_handler(request: Request, exc: InvalidRequestException):
        return JSONResponse(
            status_code=exc.code,
            content={"status": "failed", "message": f"Oops! {exc.name}"}
        )

    @app.exception_handler(InternalServerException)
    def internal_server_exception_handler(request: Request, exc: InternalServerException):
        return JSONResponse(
            status_code=exc.code,
            content={"status": "error", "message": f"Oops! {exc.name}"}
        )

    app.include_router(orders_router, prefix='/orders')

    @app.on_event('startup')
    def test():
        print('event: startup')

    @app.on_event('shutdown')
    def test1():
        print('event: shutdown')

    return app

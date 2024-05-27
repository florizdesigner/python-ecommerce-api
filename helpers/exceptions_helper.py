from fastapi import status


class InvalidRequestException(Exception):
    def __init__(self, name: str, code: int = status.HTTP_400_BAD_REQUEST):
        self.name = name
        self.code = code


class InternalServerException(Exception):
    def __init__(self, name: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.name = name
        self.code = code

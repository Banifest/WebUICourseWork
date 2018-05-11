class AuthException(Exception):
    pass


class ErrorStatus(Exception):
    detail: str
    status_code: int

    def __init__(self, status_code: int=400, status: dict={'detail': ''}) -> None:
        self.status_code = status_code
        self.detail = status

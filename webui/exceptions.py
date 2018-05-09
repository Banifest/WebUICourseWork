class AuthException(Exception):
    pass


class ErrorStatus(Exception):
    status: str
    status_code: int

    def __init__(self, status_code: int=400, status: str='') -> None:
        self.status_code = status_code
        self.status = status

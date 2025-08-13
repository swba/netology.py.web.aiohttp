class HttpError(Exception):

    def __init__(self, status_code: int, message: str | list) -> None:
        self.status_code = status_code
        self.message = message

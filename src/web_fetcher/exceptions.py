

class FetchError(Exception):
    """Custom exception for fetch errors."""

    def __init__(self, url: str, message: str, retries: int , status_code: int | None = None ):
        self.url = url
        self.status_code = status_code
        self.retries = retries
        super().__init__(message)
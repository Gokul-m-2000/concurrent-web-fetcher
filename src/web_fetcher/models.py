from dataclasses import dataclass


@dataclass
class FetchResult:
    url: str
    status_code: int | None
    title: str | None
    text: str | None
    error: str | None = None
    retries: int = 0

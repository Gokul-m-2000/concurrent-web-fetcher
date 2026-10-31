from dataclasses import dataclass

@dataclass
class CrawlerConfig:
    max_concurrency: int = 10
    timeout: float = 10.0
    retries: int = 3
    retry_delay: float = 1.0
  
    def __post_init__(self):
        if self.max_concurrency < 1:
            raise ValueError("max_concurrency must be a positive integer.")
        if self.timeout <= 0:
            raise ValueError("timeout must be a positive number.")
        if self.retries < 0:
            raise ValueError("retries must be a non-negative integer.")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be a non-negative number.")
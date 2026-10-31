from src.web_fetcher.config import CrawlerConfig


config=CrawlerConfig()

print(config)


assert config.max_concurrency==10
assert config.timeout==10.0

assert config.retries==2
assert config.retry_delay==1.0

try:
    config=CrawlerConfig(max_concurrency=5)

except ValueError:
    print(f"Caught ValueError for max_concurrency")
import asyncio
import httpx
from .config import CrawlerConfig
from .models import FetchResult
from .fetcher import fetch_with_retry
from .exceptions import FetchError
from .extractor import extract_content



async def crawler(urls: list[str], config: CrawlerConfig) -> list[FetchResult]:
    results = []
    semaphore = asyncio.Semaphore(config.max_concurrency)

    async with httpx.AsyncClient(timeout=config.timeout,follow_redirects=True) as client:
        tasks = [fetch_with_retry(url, config, client, semaphore) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for url, response in zip(urls, responses):
            if isinstance(response, FetchError):

                results.append(FetchResult(url=url, status_code=response.status_code, title=None, text=None, error=str(response), retries=response.retries))
            else:
                http_response,retries=response
                title,text=extract_content(http_response.text)
                results.append(FetchResult(url=url, status_code=http_response.status_code, title=title, text=text, error=None, retries=retries))
               
    return results
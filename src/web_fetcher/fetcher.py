import asyncio
import httpx
from .config import CrawlerConfig
from .exceptions import FetchError


async def fetch_with_retry(url : str ,
                            config: CrawlerConfig,
                            client: httpx.AsyncClient,
                            semaphore: asyncio.Semaphore) -> tuple[httpx.Response, int]:
    retries = config.retries
    retry_delay = config.retry_delay

    for attempt in range(retries + 1):
        try:
            async with semaphore:
                response = await client.get(url)
                
                
            response.raise_for_status()   
            return response,attempt
            
        except httpx.HTTPStatusError as e:
            status= e.response.status_code
            if status not in (408,429) and status < 500:
                raise FetchError(url=url,
                                message=str(e) or f"{type(e).__name__} while requesting {url}",
                                retries=attempt,
                                status_code=status) from e

            if attempt == retries:
                
                raise FetchError(url=url,
                                message=str(e),     
                    retries=attempt,
                    status_code=status) from e
                
           
        except httpx.RequestError as e:
            
            if attempt == retries:
                raise FetchError(url=url,
                                message=str(e) or f"{type(e).__name__} while requesting {url}",
                                retries=attempt) from e

        delay = retry_delay * (2 ** attempt)
        await asyncio.sleep(delay)

    raise RuntimeError(f"Unexpected error: Failed to fetch {url} after {retries} retries.")

import asyncio
import re
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse



class Crawler:
    def __init__(self,
                 urls:list[str],
                 max_workers:int=2,
                 ):
        self.urls=urls
        self.max_workers=max_workers
        self.client :httpx.AsyncClient | None =None
        self.queue : asyncio.Queue[str] =asyncio.Queue()
        self.seen_urls : set[str] =set()
        self.results :list[dict] = []
        self.semaphore : asyncio.Semaphore = asyncio.Semaphore(max_workers)

    

    async def fetcher(self,client,url):
        response=await client.get(url)
        response.raise_for_status()

        return response

    def link_extractor(self,html, base_url):
        soup=BeautifulSoup(html, 'html.parser')

        links=soup.find_all('a', href=True)
        return [urljoin(base_url,link['href']) for link in links]
    
    def filter_links(self,links,base_url):
        domain=urlparse(base_url).hostname
        urls=[]
        for link in links:
            parsed_link=urlparse(link)
            if parsed_link.scheme not in ["https","http"]:
                continue
            elif parsed_link.hostname!=domain:
                continue
            elif parsed_link.path.lower().endswith('.pdf'):
                continue
            else:
                urls.append(link)
        # print(f"urls :{urls}")
        # print(f"duplicate removed :{list(dict.fromkeys(urls))}")
        return list(dict.fromkeys(urls))

    async def crawl_page(self,client, url):
        response=await self.fetcher(client,url)
        print(f"Fetched {url} with status code {response.status_code}")
        links=self.link_extractor(response.text,url)
        print(f"Extracted links from {url}: {links}")
        filtered_links=self.filter_links(links,url)
        print(f"Filtered links from {url}: {filtered_links}")
        return filtered_links


    async def fetch_with_limits(self,url :str):
            async with self.semaphore:
                try:
                    response=await self.fetcher(self.client,url)
                    return {
                        "url": url,
                        "status_code": response.status_code,
                        "html": response.text,
                        "error": None
                    }
    
                except Exception as e:
                    return {
                        "url": url,
                        "status_code": None,
                        "html": None,
                        "error": str(e)
    
                    }



    async def run(self) ->list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            self.client=client
            results=await asyncio.gather(*(self.fetch_with_limits(url) for url in self.urls))

        self.results=results
        return results



async def main():
    urls=[
        "https://www.iana.org/domains/reserved",
        "https://httpbin.org/html",
        "https://invalid.example",]
    crawler=Crawler(urls,max_workers=2)
    results=await crawler.run()
    for result in results:
        print(f"URL: {result['url']}, Status Code: {result['status_code']}, Error: {result['error']}")






asyncio.run(main())





    # async def run(self):
    #         async with httpx.AsyncClient(timeout=10.0) as client:
    #             self.client=client
    #             responses=await asyncio.gather(*(self.crawl_page(client, url) for url in self.urls))
    #         print(f"Responses: {responses}")
    #         return responses
    




    # async def crawl_urls(urls):
    #     async with httpx.AsyncClient(timeout=10.0) as client:
    #         responses=await asyncio.gather(*(crawl_page(client,url) for url in urls))
    #     print(f"Responses: {responses}")
    #     # for response in responses:
    #     #     print(response.status_code,response.url)
    #     return responses



    # urls = [
    #         "https://www.iana.org/domains/reserved"
    #     ]

    # print(asyncio.run(crawl_urls(urls)))



# print(asyncio.run(filter_links(["https://example.com/about", "example.com","https://google.com", "example.com","mailto:hello@example.com", "example.com","https://example.com/report.pdf", "example.com"],"https://example.com")))

# links = [
#     "https://example.com/about",
#     "https://example.com/report.pdf",
#     "https://google.com",
#     "mailto:hello@example.com",
#     "https://example.com/contact"
# ]

# print(filter_links(links, "https://example.com"))

# html = """
# <a href="/about">About Us</a>
# <a href="https://example.com/contact">Contact</a>
# """

# result =asyncio.run(link_extractor(html, "https://example.com"))
# print(result)


# html = """
# <html>
#     <body>
#         <a href="/about">About</a>
#         <a href="https://example.com/contact">Contact</a>
#         <a href="https://google.com">Google</a>
#         <a href="/report.pdf">Report</a>
#     </body>
# </html>
# """

# base_url = "https://example.com"

# links = asyncio.run(link_extractor(html, base_url))
# print("Extracted:", links)

# filtered = filter_links(links, base_url)
# print("Filtered:", filtered)
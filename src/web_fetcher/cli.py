import argparse
from .config import CrawlerConfig
import asyncio
from .crawler import crawler
from .output import save_results


def parse_arguments() -> argparse.Namespace:
    parser=argparse.ArgumentParser()

    parser.add_argument("urls",nargs="+")
    parser.add_argument("--concurrency",type=int,default=10)
    parser.add_argument("--timeout",type=float,default=10.0)
    parser.add_argument("--retries",type=int,default=3)
    parser.add_argument("--retry-delay",type=float,default=1.0)
    parser.add_argument("--output",default="results.json")


    args=parser.parse_args()
    return args

def create_config(args:argparse.Namespace) -> CrawlerConfig:

    config = CrawlerConfig(
    max_concurrency=args.concurrency,
    timeout=args.timeout,
    retries=args.retries,
    retry_delay=args.retry_delay
)

    return config


def main() -> None:
    cli_arguments=parse_arguments()
    cli_config=create_config(cli_arguments)
    results=asyncio.run(crawler(cli_arguments.urls,cli_config))
    
    save_results(results,cli_arguments.output)


if __name__=="__main__":
    main()
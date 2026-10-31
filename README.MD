# Concurrent Web Fetcher

A Python-based asynchronous web fetcher that retrieves multiple webpages concurrently, handles request failures with retries, extracts readable content, and saves the results in JSON format.

## Features

- Fetch multiple URLs concurrently using `asyncio` and HTTPX.
- Control the maximum number of concurrent requests.
- Retry failed requests with exponential backoff.
- Handle HTTP errors, timeouts, and network failures.
- Follow HTTP redirects.
- Extract page titles and readable text using BeautifulSoup.
- Save results to a JSON file.
- Configure fetching options through a command-line interface.

## Tech Stack

- Python 3.11+
- HTTPX
- Asyncio
- BeautifulSoup4
- Argparse

## Project Structure

```text
concurrent-web-fetcher/
├── src/
│   └── web_fetcher/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── crawler.py
│       ├── exceptions.py
│       ├── extractor.py
│       ├── fetcher.py
│       ├── models.py
│       └── output.py
├── tests/
├── pyproject.toml
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd concurrent-web-fetcher
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project:

```bash
pip install -e .
```

## Usage

Fetch one or more URLs:

```bash
web-fetcher https://www.python.org https://www.bbc.com
```

Specify concurrency:

```bash
web-fetcher https://www.python.org --concurrency 5
```

Configure retries and timeout:

```bash
web-fetcher https://www.python.org --retries 3 --timeout 10
```

Specify the output file:

```bash
web-fetcher https://www.python.org --output results.json
```

## Output

The fetched results are saved in JSON format, including:

- URL
- HTTP status code
- Page title
- Extracted text
- Error details, if any
- Number of retries used

## Project Status

Core asynchronous fetching, retry handling, content extraction, command-line execution, and JSON output are implemented. Additional testing and improvements are planned.


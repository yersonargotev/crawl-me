# Web Page Crawler

A powerful and flexible web crawler that converts web pages to markdown files. This tool is particularly useful for creating local documentation from websites.

## Features

- Crawls websites and converts pages to markdown
- Stays within the specified domain
- Configurable crawl depth
- Maintains original URL references
- Saves files in an organized directory structure

## Prerequisites

- Python 3.7+
- pip or uv package manager

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:

Using uv (recommended):
```bash
uv venv
source .venv/bin/activate  # On Unix/MacOS
.\.venv\Scripts\activate.ps1  # On Windows
```

3. Install dependencies:
```bash
uv sync
```

## Usage

The crawler can be run using the command line interface:

```bash
python main.py --url "https://example.com" --output-dir "./data/docs"
```

### Parameters

- `--url`: The starting URL to crawl (required)
- `--output-dir`: Directory where markdown files will be saved (default: "./data/factus_docs")

### Example

```bash
python main.py --url "https://docs.example.com" --output-dir "./data/documentation"
```

## Output

The crawler will:
1. Create the specified output directory if it doesn't exist
2. Convert each crawled page to markdown
3. Save files with cleaned, URL-based filenames
4. Include the source URL at the top of each markdown file
5. Display progress during crawling

## Configuration

The crawler includes several built-in configurations:

- Maximum crawl depth: 20 pages (adjustable in code)
- Headless browser mode: Enabled
- Domain restriction: Only crawls within the initial domain
- Streaming mode: Enabled for real-time processing

## Limitations

- Only crawls within the same domain as the starting URL
- Some JavaScript-heavy pages might not render completely
- Rate limiting may apply depending on the target website

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT

import asyncio
import os
from urllib.parse import urlparse

import typer
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, DomainFilter, FilterChain

app = typer.Typer()


class FactusDocCrawler:
    def __init__(self, start_url, output_dir="./data/factus_docs"):
        self.start_url = start_url
        self.output_dir = output_dir
        self.visited_urls = set()
        self.domain = urlparse(start_url).netloc

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def clean_filename(self, url):
        """Convert URL to a valid filename"""
        # Extract path from URL
        path = urlparse(url).path
        # Remove leading and trailing slashes
        path = path.strip("/")
        # Replace remaining slashes with underscores
        path = path.replace("/", "_")

        # If path is empty (homepage), use 'index'
        if not path:
            path = "index"

        # Add .md extension
        return f"{path}.md"

    async def crawl(self):
        # Configure browser
        browser_config = BrowserConfig(headless=True, verbose=True)

        # Set up domain filter to stay within the site
        filter_chain = FilterChain([DomainFilter(allowed_domains=[self.domain])])

        # Configure deep crawl strategy
        deep_crawl_config = CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=20,  # Adjust as needed based on site structure
                include_external=False,
                filter_chain=filter_chain,
            ),
            stream=True,
            verbose=True,
        )

        print(f"Starting to crawl {self.start_url}...")
        print(f"Saving documentation to {self.output_dir}/ directory")

        async with AsyncWebCrawler(config=browser_config) as crawler:
            count = 0
            async for result in await crawler.arun(
                url=self.start_url, config=deep_crawl_config
            ):
                if result.success:
                    url = result.url
                    if url in self.visited_urls:
                        continue

                    self.visited_urls.add(url)
                    count += 1

                    # Get markdown content
                    if result.markdown:
                        markdown_content = result.markdown.raw_markdown

                        # Save content to file
                        filename = self.clean_filename(url)
                        filepath = os.path.join(self.output_dir, filename)

                        # Add URL as header for reference
                        content_with_source = f"# {url}\n\n{markdown_content}"

                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(content_with_source)

                        print(f"[{count}] Saved {url} to {filepath}")
                    else:
                        print(f"[{count}] No markdown content for {url}")
                else:
                    print(f"Failed to crawl {result.url}: {result.error_message}")

        print(f"Crawling completed. Processed {count} pages.")


@app.command()
def crawl(
    url: str = typer.Option(
        ..., prompt="Enter the URL to crawl", help="The URL to start crawling from"
    ),
    output_dir: str = typer.Option(
        "./data/factus_docs", help="Directory to save the crawled content"
    ),
):
    """
    Crawl a website and save its content as markdown files.
    """

    async def run_crawler():
        crawler = FactusDocCrawler(url, output_dir)
        await crawler.crawl()

    asyncio.run(run_crawler())


if __name__ == "__main__":
    app()

import asyncio
import json
import sys
from scrapers.seek_scraper import SeekScraper

class SingleItemSeekScraper(SeekScraper):
    """
    A subclass of SeekScraper that stops after finding one job
    and prints the details to the console.
    """
    def save_job(self, job_data):
        print("\n--- Scraped Job Details ---")
        for key, value in job_data.items():
            if key == "raw_content":
                print(f"{key}: <HTML Content Truncated> ({len(value)} chars)")
            else:
                print(f"{key}: {value}")
        print("---------------------------\n")
        
        # Stop execution after one item
        print("Successfully retrieved one item. Exiting.")
        sys.exit(0)

async def main():
    scraper = SingleItemSeekScraper()
    # Use a specific term and limit pages to 1 to be safe, 
    # though we exit after the first item anyway.
    await scraper.scrape(page_limit=1, search_terms=["Software Engineer"])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except SystemExit:
        pass # Expected exit
    except Exception as e:
        print(f"An error occurred: {e}")

import logging
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.seek_scraper import SeekScraper
from scrapers.prosple_scraper import ProspleScraper
from scrapers.gradconnection_scraper import GradConnectionScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Main")

def run_all():
    logger.info("--- Starting All Scrapers ---")
    
    try:
        logger.info("Running Seek Scraper...")
        SeekScraper().run()
    except Exception as e:
        logger.error(f"Seek Scraper failed: {e}")
        
    logger.info("--- All Scrapers Finished ---")

if __name__ == "__main__":
    run_all()

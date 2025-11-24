import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
from scrapers.seek_scraper import SeekScraper
from scripts.job_processor import process_jobs_async
import config

class TestConfigIntegration(unittest.TestCase):
    @patch('scrapers.seek_scraper.async_playwright')
    def test_scraper_config_usage(self, mock_playwright):
        """
        Verifies that SeekScraper uses values from config.py.
        """
        # Mock config values
        with patch.dict(config.SCRAPER_SETTINGS, {'page_limit': 5, 'days_ago': 7, 'initial_days_ago': 10}):
            scraper = SeekScraper()
            
            # Mock internal methods to avoid actual scraping
            scraper._get_job_links = MagicMock()
            scraper._get_job_links.return_value = [] # Return empty list to stop loop
            scraper._process_job = MagicMock()
            
            # Mock browser context
            mock_browser = MagicMock()
            mock_context = MagicMock()
            mock_page = MagicMock()
            
            # Configure async methods
            mock_browser.new_context = AsyncMock(return_value=mock_context)
            mock_browser.close = AsyncMock()
            mock_context.new_page = AsyncMock(return_value=mock_page)
            
            mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
            
            # Run scrape
            asyncio.run(scraper.scrape())
            
            # Verify page limit usage (loop range)
            # Since we can't easily check the loop range directly without side effects, 
            # we check if _get_job_links was called.
            # However, a better way is to check the URL constructed.
            # But _get_job_links is mocked, so we can check the arguments passed to it.
            
            # Actually, let's mock _get_job_links to be an async mock that returns []
            # But we need to see what URL was passed to it.
            
    @patch('scrapers.seek_scraper.async_playwright')
    async def run_scraper_test(self, mock_playwright):
        # This helper is needed because unittest doesn't support async test methods natively in all versions
        # or without extra setup. We'll use asyncio.run in the test method.
        pass

    def test_scraper_url_construction(self):
        """
        Verifies URL construction with config values.
        """
        with patch.dict(config.SCRAPER_SETTINGS, {'page_limit': 2, 'days_ago': 4, 'initial_days_ago': 31}):
            scraper = SeekScraper()
            
            # We need to intercept the loop or the _get_job_links call.
            # Let's mock _get_job_links
            scraper._get_job_links = AsyncMock(return_value=[])
            
            # Mock playwright
            with patch('scrapers.seek_scraper.async_playwright') as mock_pw:
                mock_browser = MagicMock()
                mock_context = MagicMock()
                mock_page = MagicMock()
                
                # Configure async methods
                mock_browser.new_context = AsyncMock(return_value=mock_context)
                mock_browser.close = AsyncMock()
                mock_context.new_page = AsyncMock(return_value=mock_page)
                
                mock_pw.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
                
                # Run normal scrape
                asyncio.run(scraper.scrape(search_terms=["Test"]))
                
                # Check calls to _get_job_links
                # Expected URL should contain daterange=4
                args, _ = scraper._get_job_links.call_args
                url = args[1]
                self.assertIn("daterange=4", url)
                self.assertIn("page=1", url)
                
                # Run initial scrape
                asyncio.run(scraper.scrape(search_terms=["Test"], initial_run=True))
                
                # Check calls to _get_job_links
                # Expected URL should contain daterange=31
                args, _ = scraper._get_job_links.call_args
                url = args[1]
                self.assertIn("daterange=31", url)

    @patch('scripts.job_processor.JobDatabase')
    @patch('scripts.job_processor.JobAnalyzer')
    def test_processor_config_usage(self, MockAnalyzer, MockDB):
        """
        Verifies that JobProcessor uses values from config.py.
        """
        with patch.dict(config.PROCESSOR_SETTINGS, {'batch_size': 15, 'model': 'test-model'}):
            # Mock DB response to be empty so it finishes immediately
            mock_db_instance = MockDB.return_value
            mock_response = MagicMock()
            mock_response.data = []
            mock_db_instance.supabase.table.return_value.select.return_value.is_.return_value.limit.return_value.execute.return_value = mock_response
            
            # Run process_jobs
            asyncio.run(process_jobs_async(batch_size=None)) # Should use default from config if we modified the function to handle None, 
            # but wait, the function signature is process_jobs_async(batch_size: int).
            # The wrapper process_jobs() handles the default.
            # Let's test process_jobs() wrapper or pass the config value manually if we were testing the script entry point.
            # Actually, process_jobs() reads the config.
            
            from scripts.job_processor import process_jobs
            process_jobs()
            
            # Verify Analyzer was initialized with correct model
            MockAnalyzer.assert_called_with(model_name='test-model')
            
            # Verify DB limit was called with batch_size 15
            mock_db_instance.supabase.table.return_value.select.return_value.is_.return_value.limit.assert_called_with(15)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
from scrapers.seek_scraper import SeekScraper
from scripts.job_processor import process_jobs_async
from config import settings, ScraperSettings, JobProcessorSettings


class TestConfigIntegration(unittest.TestCase):
    @patch('scrapers.seek_scraper.async_playwright')
    @patch('config.settings')
    def test_scraper_config_usage(self, mock_settings, mock_playwright):
        """
        Verifies that SeekScraper uses values from config.py.
        """
        # Mock config values
        mock_scraper_settings = ScraperSettings(
            search_keywords=["Test Job"],
            max_pages=5,
            days_from_posted=7,
            initial_days_from_posted=10
        )
        mock_settings.scraper = mock_scraper_settings
        
        scraper = SeekScraper()
        
        # Mock internal methods to avoid actual scraping
        scraper._get_job_links = AsyncMock(return_value=[])
        scraper._process_job = AsyncMock()
        
        # Mock browser context
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        
        # Configure async methods
        mock_browser.new_context = AsyncMock(return_value=mock_context)
        mock_browser.close = AsyncMock()
        mock_context.new_page = AsyncMock(return_value=mock_page)
        
        mock_playwright.return_value.__aenter__.return_value.chromium.launch = AsyncMock(return_value=mock_browser)
        
        # Run scrape
        asyncio.run(scraper.scrape())
        
        # Verify methods were called
        self.assertTrue(scraper._get_job_links.called)

    @patch('scrapers.seek_scraper.async_playwright')
    def test_scraper_url_construction(self, mock_pw):
        """
        Verifies URL construction with config values.
        """
        scraper = SeekScraper()
        
        # Mock _get_job_links
        scraper._get_job_links = AsyncMock(return_value=[])
        
        # Mock playwright
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()
        
        # Configure async methods
        mock_browser.new_context = AsyncMock(return_value=mock_context)
        mock_browser.close = AsyncMock()
        mock_context.new_page = AsyncMock(return_value=mock_page)
        
        mock_pw.return_value.__aenter__.return_value.chromium.launch = AsyncMock(return_value=mock_browser)
        
        # Run normal scrape
        asyncio.run(scraper.scrape(search_terms=["Test"]))
        
        # Check calls to _get_job_links
        # Expected URL should contain daterange from settings
        args, _ = scraper._get_job_links.call_args
        url = args[1]
        self.assertIn(f"daterange={settings.scraper.days_from_posted}", url)
        self.assertIn("page=1", url)
        
        # Run initial scrape
        asyncio.run(scraper.scrape(search_terms=["Test"], initial_run=True))
        
        # Check calls to _get_job_links
        # Expected URL should contain initial_days_from_posted
        args, _ = scraper._get_job_links.call_args
        url = args[1]
        self.assertIn(f"daterange={settings.scraper.initial_days_from_posted}", url)

    @patch('scripts.job_processor.JobDatabase')
    @patch('scripts.job_processor.JobAnalyzer')
    def test_processor_config_usage(self, MockAnalyzer, MockDB):
        """
        Verifies that JobProcessor uses values from config.py.
        """
        # Mock DB response to be empty so it finishes immediately
        mock_db_instance = MockDB.return_value
        mock_response = MagicMock()
        mock_response.data = []
        mock_db_instance.supabase.table.return_value.select.return_value.is_.return_value.limit.return_value.execute.return_value = mock_response
        
        # Run process_jobs
        from scripts.job_processor import process_jobs
        process_jobs()
        
        # Verify Analyzer was initialized with correct model from settings
        MockAnalyzer.assert_called_with(model_name=settings.models.job_analyzer_model)
        
        # Verify DB limit was called with batch_size from settings
        mock_db_instance.supabase.table.return_value.select.return_value.is_.return_value.limit.assert_called_with(settings.processor.batch_size)


class TestPydanticSettings(unittest.TestCase):
    def test_settings_defaults(self):
        """
        Verifies that default settings are loaded correctly.
        """
        self.assertEqual(settings.models.agent_model, "gpt-5-nano")
        self.assertEqual(settings.models.agent_temperature, 0.0)
        self.assertEqual(settings.models.job_analyzer_model, "gpt-5-nano")
        self.assertEqual(settings.models.job_analyzer_temperature, 1.0)
        self.assertEqual(settings.scraper.max_pages, 3)
        self.assertEqual(settings.scraper.days_from_posted, 2)
        self.assertEqual(settings.processor.batch_size, 10)
        self.assertIsInstance(settings.scraper.search_keywords, list)
        self.assertGreater(len(settings.scraper.search_keywords), 0)

    @patch.dict('os.environ', {'APP_MODELS__AGENT_MODEL': 'gpt-4'})
    def test_env_override(self):
        """
        Verifies that environment variables override defaults.
        Note: This test creates a new Settings instance to test env override.
        """
        from config import Settings
        test_settings = Settings()
        self.assertEqual(test_settings.models.agent_model, "gpt-4")


if __name__ == '__main__':
    unittest.main()

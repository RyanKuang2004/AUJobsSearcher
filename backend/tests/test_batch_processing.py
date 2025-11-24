import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from scripts.job_processor import process_jobs_async

class TestBatchProcessing(unittest.TestCase):
    def test_batch_execution(self):
        """
        Tests that process_jobs_async runs without errors and attempts to process jobs.
        We mock the DB and Analyzer to avoid real API calls.
        """
        
        # Mock DB
        mock_db = MagicMock()
        mock_response = MagicMock()
        # Return 3 dummy jobs
        mock_response.data = [
            {"id": "1", "description": "Job 1", "job_title": "Title 1"},
            {"id": "2", "description": "Job 2", "job_title": "Title 2"},
            {"id": "3", "description": "Job 3", "job_title": "Title 3"},
        ]
        # First call returns jobs, second call returns empty list to break loop
        mock_db.supabase.table.return_value.select.return_value.is_.return_value.limit.return_value.execute.side_effect = [mock_response, MagicMock(data=[])]
        
        # Mock Analyzer
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_job_description_async = AsyncMock(return_value={"skills": "test"})
        
        # Patch the classes in the module
        import scripts.job_processor
        scripts.job_processor.JobDatabase = MagicMock(return_value=mock_db)
        scripts.job_processor.JobAnalyzer = MagicMock(return_value=mock_analyzer)
        
        # Run the async function
        asyncio.run(process_jobs_async(batch_size=3))
        
        # Verify
        self.assertEqual(mock_analyzer.analyze_job_description_async.call_count, 3)
        self.assertEqual(mock_db.update_llm_analysis.call_count, 3)
        print("Batch processing test passed: 3 jobs processed concurrently.")

if __name__ == "__main__":
    unittest.main()

import logging
import time
from db.database import JobDatabase
from analyzers.job_analyzer import JobAnalyzer
from config import PROCESSOR_SETTINGS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JobProcessor")

import asyncio

def process_jobs(batch_size: int = None):
    bs = batch_size if batch_size else PROCESSOR_SETTINGS['batch_size']
    asyncio.run(process_jobs_async(bs))

async def process_jobs_async(batch_size: int):
    db = JobDatabase()
    analyzer = JobAnalyzer(model_name=PROCESSOR_SETTINGS['model'])
    
    logger.info(f"Starting Job Processor (Batch Size: {batch_size})...")
    logger.info("Connecting to database...")
    
    while True:
        try:
            # Fetch unanalyzed jobs
            response = db.supabase.table("job_postings") \
                .select("*") \
                .is_("llm_analysis", "null") \
                .limit(batch_size) \
                .execute()
            
            jobs = response.data
            
            if not jobs:
                logger.info("No unanalyzed jobs found.")
                break
                
            logger.info(f"Found {len(jobs)} unanalyzed jobs. Processing batch...")
            
            tasks = []
            for job in jobs:
                tasks.append(process_single_job(db, analyzer, job))
            
            # Run batch concurrently
            await asyncio.gather(*tasks)
            
            # Brief sleep to avoid hammering if loop continues immediately
            await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in processing loop: {e}")
            break

    logger.info("Job Processor Finished.")

async def process_single_job(db, analyzer, job):
    job_id = job['id']
    description = job.get('description', '')
    
    if not description:
        logger.warning(f"Job {job_id} has no description. Skipping.")
        return
        
    logger.info(f"Analyzing Job: {job.get('job_title')} ({job_id})")
    
    try:
        analysis = await analyzer.analyze_job_description_async(description)
        if analysis:
            logger.info(f"Generated analysis of {len(str(analysis))} characters for job {job_id}")
            # Note: DB update is synchronous for now, which is fine as it's fast enough
            # or we could make it async if the DB client supports it.
            # For now, we'll just run it in the thread.
            db.update_llm_analysis(job_id, analysis)
            logger.info(f"Successfully analyzed and updated job {job_id}")
        else:
            logger.warning(f"Analysis returned empty for job {job_id}")

    except Exception as e:
        logger.error(f"Failed to analyze job {job_id}: {e}")

if __name__ == "__main__":
    process_jobs()

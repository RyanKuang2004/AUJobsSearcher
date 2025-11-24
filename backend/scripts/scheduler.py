import schedule
import time
import subprocess
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_process_and_stream_output(command, env):
    """
    Runs a subprocess and streams its stdout/stderr to the logger in real-time.
    """
    process = subprocess.Popen(
        command,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, # Merge stderr into stdout
        text=True,
        bufsize=1,  # Line buffered
        universal_newlines=True
    )

    # We need to read stdout and stderr. 
    # For simplicity in this script, we'll read line by line.
    # Note: This simple blocking read might block if one pipe fills up while we read the other,
    # but for typical logging it's usually fine or we can use threads/selectors for robustness.
    # Given the simple nature, we'll just read stdout then stderr after process finishes 
    # OR better, use a loop to read available output. 
    # Actually, the most robust simple way without threads is to just pipe stdout to logger
    # but we want to capture it.
    
    # Let's use a simpler approach: redirect stdout/stderr to PIPE and read line by line
    # But to do it truly "live", we need to iterate.
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logger.info(f"[{command[-1]}] {output.strip()}")
            
    # Check for any remaining stderr
    # stderr is merged into stdout, so no need to read it separately
        
    return process.poll()

def run_scraper():
    logger.info("Starting scheduled scraper run...")
    try:
        # Run the scraper script as a subprocess
        # This ensures a fresh process for each run
        env = os.environ.copy()
        
        logger.info("Launching Seek Scraper...")
        return_code = run_process_and_stream_output(
            ["python", "-m", "scrapers.seek_scraper"],
            env=env
        )
        
        if return_code == 0:
            logger.info("Scraper finished successfully.")
            
            # Run the job processor
            logger.info("Starting Job Processor...")
            processor_return_code = run_process_and_stream_output(
                ["python", "-m", "scripts.job_processor"],
                env=env
            )
            
            if processor_return_code == 0:
                logger.info("Job Processor finished successfully.")
            else:
                logger.error(f"Job Processor failed with return code {processor_return_code}.")
                
        else:
            logger.error(f"Scraper failed with return code {return_code}.")
            
    except Exception as e:
        logger.error(f"Error running scraper: {e}")

def main():
    logger.info("Scheduler started. Waiting for 06:00...")
    
    # Schedule the job every day at 06:00
    schedule.every().day.at("06:00").do(run_scraper)
    
    # Also run immediately on startup if requested (optional, good for testing)
    if os.getenv("RUN_ON_STARTUP", "false").lower() == "true":
        logger.info("Running on startup...")
        run_scraper()

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

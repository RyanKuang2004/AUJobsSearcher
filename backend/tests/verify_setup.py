import uuid
from db import JobDatabase

def verify_setup():
    print("--- Verifying Database Setup ---")
    
    try:
        db = JobDatabase()
        print("✅ Connection to Supabase successful.")
    except Exception as e:
        print("❌ Connection failed.")
        print(f"Error: {e}")
        print("Tip: Check your .env file and ensure SUPABASE_URL and SUPABASE_KEY are correct.")
        return

    # Test Insert
    test_id = str(uuid.uuid4())
    test_url = f"https://test.com/job/{test_id}"
    
    print(f"\nAttempting to insert a test record (ID: {test_id})...")
    
    test_job = {
        "source_urls": [test_url],
        "platforms": ["test_platform"],
        "title": "Test Job Title",
        "company": "Test Company",
        "locations": ["Sydney"],
        "raw_content": "This is a test job description.",
        "llm_analysis": {
            "summary": "Test summary",
            "skills": ["Python", "Testing"]
        }
    }
    
    try:
        inserted = db.upsert_job(test_job)
        if inserted:
            print("✅ Insert successful.")
            print(f"Inserted Record: {inserted.get('id')}")
        else:
            print("❌ Insert returned no data (but no error raised).")
    except Exception as e:
        print("❌ Insert failed.")
        print(f"Error: {e}")
        print("Tip: Did you run the schema.sql script in the Supabase SQL Editor?")
        return

    # Test Retrieval
    print("\nAttempting to retrieve the test record...")
    try:
        retrieved = db.get_job_by_fingerprint("Test Company", "Test Job Title")
        if retrieved and retrieved['title'] == "Test Job Title":
            print("✅ Retrieval successful.")
            print(f"Retrieved Analysis: {retrieved.get('llm_analysis')}")
        else:
            print("❌ Retrieval failed or data mismatch.")
    except Exception as e:
        print(f"❌ Retrieval error: {e}")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify_setup()

from db.database import JobDatabase
import time

def test_deduplication():
    print("--- Testing Deduplication Logic ---")
    db = JobDatabase()
    
    # 1. Insert First Job (Seek, Sydney)
    job1 = {
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "platform": "seek",
        "location": "Sydney",
        "source_url": "http://seek.com/job/1",
        "raw_content": "Original content"
    }
    
    print("\n1. Inserting Job 1 (Seek, Sydney)...")
    try:
        res1 = db.upsert_job(job1)
        print(f"   Result: ID={res1['id']}, Locs={res1['locations']}, Platforms={res1['platforms']}")
    except Exception as e:
        print(f"   Error: {e}")
        return

    # 2. Insert Duplicate Job (LinkedIn, Melbourne)
    job2 = {
        "title": "Senior Python Developer",
        "company": "TechCorp",  # Same company + title = Same Fingerprint
        "platform": "linkedin",
        "location": "Melbourne",
        "source_url": "http://linkedin.com/job/99",
        "raw_content": "Newer content"
    }
    
    print("\n2. Inserting Job 2 (LinkedIn, Melbourne) - Should MERGE...")
    try:
        res2 = db.upsert_job(job2)
        print(f"   Result: ID={res2['id']}, Locs={res2['locations']}, Platforms={res2['platforms']}")
        
        # Verification
        if res1['id'] == res2['id']:
            print("   ✅ SUCCESS: IDs match (Record was updated, not duplicated).")
        else:
            print("   ❌ FAIL: IDs do not match (Duplicate created).")
            
        if "Sydney" in res2['locations'] and "Melbourne" in res2['locations']:
             print("   ✅ SUCCESS: Locations merged correctly.")
        else:
             print(f"   ❌ FAIL: Locations not merged: {res2['locations']}")
             
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_deduplication()

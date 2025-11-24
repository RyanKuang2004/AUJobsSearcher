import os
import sys
from dotenv import load_dotenv

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.agent.tools import execute_supabase_code

def test_tool():
    print("Testing execute_supabase_code...")
    
    # Manually provide the code that the LLM would generate
    code = """
response = supabase.table("job_postings").select("*", count="exact", head=True).execute()
"""
    print(f"Code: {code}")
    
    try:
        result = execute_supabase_code.invoke(code)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tool()

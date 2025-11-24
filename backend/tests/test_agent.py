import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.agent.agent import agent

def test_agent():
    print("Invoking agent...")
    try:
        # The input format depends on deepagents, but typically it accepts a list of messages or a string input
        # Let's try with a standard messages list
        response = agent.invoke({"messages": [{"role": "user", "content": "Count the number of job postings in the database."}]})
        print("Response:", response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_agent()

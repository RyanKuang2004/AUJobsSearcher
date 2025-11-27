import sys
import os
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.agent.agent import agent

def format_message(msg):
    if isinstance(msg, HumanMessage):
        return f"🧑 User: {msg.content}"
    if isinstance(msg, AIMessage):
        return f"🤖 AI: {msg.content}"
    if isinstance(msg, ToolMessage):
        return f"🛠️ Tool Response: {msg.content}"
    return str(msg)

def pretty_print_agent_response(response):
    print("\n=== Agent Response ===\n")
    
    messages = response.get("messages", [])
    for m in messages:
        print(format_message(m))
        print()

    if "usage_metadata" in response:
        print("=== Token Usage ===")
        print(response["usage_metadata"])

def test_agent():
    print("Invoking agent...")
    try:
        # The input format depends on deepagents, but typically it accepts a list of messages or a string input
        # Let's try with a standard messages list
        response = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": "Count the number of job postings in the database."}
                    ]
            }
        )
        pretty_print_agent_response(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_agent()

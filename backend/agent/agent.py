from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent
from dotenv import load_dotenv
from .prompts import INSTRUCTIONS, QUERY_WORKFLOW_INSTRUCTIONS
from .tools import execute_supabase_code

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend
from uuid import uuid4
from db.conversation_database import ConversationDatabase
from config import settings

load_dotenv()

def run_agent_message(session_id, user_message):
    """
    - Loads past history for this user (from DB)
    - Starts a new thread
    - Sends messages to DeepAgent
    - Saves new history back to DB
    """

    # Load previous conversation history
    history_store = ConversationDatabase()
    prior_messages = history_store.get_messages(session_id)

    # Create new thread ID each time (simulating "different threads")
    thread_id = str(uuid4())

    # Build message list for agent invocation
    messages = []

    # Include prior messages *as system context* (not as user utterances)
    if prior_messages:
        history_text = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in prior_messages
        )
        messages.append({
            "role": "system",
            "content": f"Here is our previous conversation:\n{history_text}"
        })

    # Add the new user message
    messages.append({"role": "user", "content": user_message})

    # --- Agent call ---
    result = agent.invoke({"messages": messages}, thread_id=thread_id)

    # Extract assistant reply
    reply = result["messages"][-1]["content"]

    history_store.save_message(session_id, "user", user_message)
    history_store.save_message(session_id, "assistant", reply)

    return reply

model = ChatOpenAI(
    model=settings.models.agent_model,
    temperature=settings.models.agent_temperature
)


supabase_query_agent = {
    "name": "supabase-query-agent",
    "description": "Agent capable of querying the Supabase database for job postings.",
    "system_prompt": QUERY_WORKFLOW_INSTRUCTIONS,
    "tools": [execute_supabase_code],
}

# Create the agent
agent = create_deep_agent(
    model=model,
    tools=[execute_supabase_code],
    system_prompt=INSTRUCTIONS,
    subagents=[supabase_query_agent],
)

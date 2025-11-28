from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend
from uuid import uuid4

class ConversationHistoryStore:
    """
    Minimal example: replace in-memory dict with Supabase queries.
    Keys: (user_id) -> list of messages (role, content)
    """
    def __init__(self):
        self._db = {}  # <- replace with Supabase DB calls

    def get_history(self, user_id):
        return self._db.get(user_id, [])

    def save_history(self, user_id, messages):
        self._db[user_id] = messages  # overwrite or append depending on design


history_store = ConversationHistoryStore()

def make_backend(runtime):
    return CompositeBackend(
        default=StateBackend(runtime),  # only short-term memory by default
    )


def run_agent_message(user_id, user_message):
    """
    - Loads past history for this user (from DB)
    - Starts a new thread
    - Sends messages to DeepAgent
    - Saves new history back to DB
    """

    # Load previous conversation history
    prior_messages = history_store.get_history(user_id)

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

    # Save updated history
    updated_history = prior_messages + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply},
    ]
    history_store.save_history(user_id, updated_history)

    return reply
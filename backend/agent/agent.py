from langchain_openai import ChatOpenAI
from deepagents import create_deep_agent
from dotenv import load_dotenv
from .prompts import INSTRUCTIONS, QUERY_WORKFLOW_INSTRUCTIONS
from .tools import execute_supabase_code

load_dotenv()

model = ChatOpenAI(model="gpt-5-nano", temperature=0)


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

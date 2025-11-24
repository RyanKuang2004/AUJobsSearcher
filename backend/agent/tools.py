"""Supabase Tools.

This module provides utilities for interacting with the Supabase database,
allowing the execution of Python code to query job postings.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_core.tools import tool

load_dotenv()

def get_supabase_client() -> Client:
    """Get the Supabase client, initializing it if necessary."""
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")
    return create_client(url, key)

supabase_client = get_supabase_client()

@tool(parse_docstring=True)
def execute_supabase_code(
    code: str,
) -> str:
    """Execute Python code to query the Supabase database.

    This tool executes Python code that uses the `supabase` client to query the `job_postings` table.
    The code should assume a `supabase` variable is available (the client).
    The code should assign the result of the query to a variable named `response`.

    Args:
        code: The Python code to execute.

    Returns:
        The result of the execution (the value of `response` or an error message).
    """
    try:
        print(f"Executing Code:\n{code}")
        
        # Clean up code block formatting if present
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        
        code = code.strip()

        # Execute the code
        local_scope = {"supabase": supabase_client}
        exec(code, {}, local_scope)
        
        result = local_scope.get("response")
        return str(result)
    except Exception as e:
        return f"Error executing code: {str(e)}"

"""Supabase Tools.

This module provides utilities for interacting with the Supabase database,
allowing the execution of Python code to query job postings.
"""

from supabase import create_client, Client
from langchain_core.tools import tool
from db import BaseDatabase

_db_instance = BaseDatabase()
supabase_client = _db_instance.supabase

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

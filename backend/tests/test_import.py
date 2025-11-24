try:
    from langchain.agents import create_tool_calling_agent
    print("Import create_tool_calling_agent successful")
except ImportError as e:
    print(f"Import create_tool_calling_agent failed: {e}")

try:
    from langgraph.prebuilt import ToolNode
    print("Import ToolNode from langgraph.prebuilt successful")
except ImportError as e:
    print(f"Import ToolNode from langgraph.prebuilt failed: {e}")

try:
    from langgraph.prebuilt.tool_node import ToolNode
    print("Import ToolNode from langgraph.prebuilt.tool_node successful")
except ImportError as e:
    print(f"Import ToolNode from langgraph.prebuilt.tool_node failed: {e}")

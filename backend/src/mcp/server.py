"""
MCP Server initialization.
Provides the MCP server instance for tool registration.
"""
# Placeholder for MCP server - actual implementation may vary by MCP version
class DummyMCP:
    def __init__(self, name: str):
        self.name = name

# Initialize MCP server
mcp = DummyMCP("todo-ai-chatbot")


def get_mcp_server():
    """Get the MCP server instance."""
    return mcp

from agent_framework.providers.groq_provider import GroqProvider
from agent_framework.tools.base_tool import BaseTool
from unittest.mock import MagicMock


class FakeTool(BaseTool):
    def __init__(self, name="fake", description="A fake tool"):
        super().__init__(name=name, description=description)

    def argument_schema(self):
        return {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        }

    def execute(self, arguments):
        return {}


# --- format_tools() ---

def test_format_tools_empty_list():
    result = GroqProvider.format_tools([])
    assert result == []

def test_format_tools_none():
    result = GroqProvider.format_tools(None)
    assert result == []

def test_format_tools_single_tool():
    tool = FakeTool(name="search", description="Search the web")
    result = GroqProvider.format_tools([tool])

    assert len(result) == 1
    assert result[0]["type"] == "function"
    assert result[0]["function"]["name"] == "search"
    assert result[0]["function"]["description"] == "Search the web"
    assert result[0]["function"]["parameters"]["properties"]["query"]["type"] == "string"

def test_format_tools_multiple_tools():
    tool_a = FakeTool(name="tool_a", description="First tool")
    tool_b = FakeTool(name="tool_b", description="Second tool")
    result = GroqProvider.format_tools([tool_a, tool_b])

    assert len(result) == 2
    assert result[0]["function"]["name"] == "tool_a"
    assert result[1]["function"]["name"] == "tool_b"
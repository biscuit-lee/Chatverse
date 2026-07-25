import pytest
from agent_framework.tools.tool_registry import ToolRegistry
from agent_framework.tools.base_tool import BaseTool

class FakeTool(BaseTool):
    def __init__(self, name="fake_tool"):
        super().__init__(name=name, description="A fake tool for testing")

    def argument_schema(self):
        return {"type": "object", "properties": {}}

    def execute(self, arguments):
        return {"done": True}


# --- register() ---

def test_register_adds_tool():
    registry = ToolRegistry()
    tool = FakeTool(name="my_tool")
    registry.register(tool)
    assert registry.get("my_tool") is tool

def test_register_duplicate_raises_error():
    registry = ToolRegistry()
    registry.register(FakeTool(name="my_tool"))
    with pytest.raises(ValueError, match="already registered"):
        registry.register(FakeTool(name="my_tool"))


# --- get() ---

def test_get_existing_tool():
    registry = ToolRegistry()
    tool = FakeTool(name="search")
    registry.register(tool)
    assert registry.get("search") is tool

def test_get_nonexistent_tool_returns_none():
    registry = ToolRegistry()
    assert registry.get("does_not_exist") is None


# --- all() ---

def test_all_returns_empty_list():
    registry = ToolRegistry()
    assert registry.all() == []

def test_all_returns_all_registered_tools():
    registry = ToolRegistry()
    tool_a = FakeTool(name="tool_a")
    tool_b = FakeTool(name="tool_b")
    registry.register(tool_a)
    registry.register(tool_b)
    assert registry.all() == [tool_a, tool_b]
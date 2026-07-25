
from unittest.mock import MagicMock
from agent_framework.agents.agent import Agent
from agent_framework.tools.base_tool import BaseTool

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


def test_register_one_tool():
    agent = Agent(
        name="Test Agent",
        description="A test agent",
        tools=[FakeTool()],
        provider=MagicMock(),
    )

    assert agent.tool_registry.get("fake") is not None


def test_register_empty_tool():
    agent = Agent(
        name="Test Agent",
        description="A test agent",
        tools=[],
        provider=MagicMock(),
    )

    assert agent.tool_registry.get("fake") is None

def test_register_multiple_tools():
    agent = Agent(
        name="Test Agent",
        description="A test agent",
        tools=[FakeTool(name="tool1"), FakeTool(name="tool2")],
        provider=MagicMock(),
    )

    assert len(agent.tool_registry.tools) == 2
    assert agent.tool_registry.get("tool1") is not None
    assert agent.tool_registry.get("tool2") is not None

def test_agent_properties():
    agent = Agent(
        name="My Agent",
        description="Helps users",
        tools=[],
        provider=MagicMock(),
    )
    assert agent.name == "My Agent"
    assert agent.description == "Helps users"
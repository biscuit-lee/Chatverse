import pytest
from unittest.mock import MagicMock
from agent_framework.agents.registry import AgentRegistry
from agent_framework.agents.agent import Agent
from agent_framework.tools.base_tool import BaseTool


class FakeTool(BaseTool):
    def __init__(self, name="fake", description="A fake tool"):
        super().__init__(name=name, description=description)

    def argument_schema(self):
        return {"type": "object", "properties": {}}

    def execute(self, arguments):
        return {}


def make_agent(id: str, name: str = "TestAgent") -> Agent:
    return Agent(
        id=id,
        name=name,
        description="A test agent",
        tools=[FakeTool()],
        provider=MagicMock(),
    )


def test_register_adds_agent():
    registry = AgentRegistry()
    agent = make_agent(id="a1")
    registry.register(agent)
    assert registry.get("a1") is agent


def test_register_duplicate_id_raises_error():
    registry = AgentRegistry()
    registry.register(make_agent(id="a1"))
    with pytest.raises(ValueError, match="Agent ID already exists"):
        registry.register(make_agent(id="a1"))


def test_get_existing_agent():
    registry = AgentRegistry()
    agent = make_agent(id="find-me")
    registry.register(agent)
    assert registry.get("find-me") is agent


def test_get_nonexistent_agent_returns_none():
    registry = AgentRegistry()
    assert registry.get("does-not-exist") is None


def test_get_by_name():
    registry = AgentRegistry()
    agent = make_agent(id="a1", name="UniqueName")
    registry.register(agent)
    assert registry.get_by_name("UniqueName") is agent


def test_get_by_name_nonexistent_returns_none():
    registry = AgentRegistry()
    assert registry.get_by_name("NoOne") is None


def test_all_returns_empty_list_initially():
    registry = AgentRegistry()
    assert registry.all() == []


def test_all_returns_all_registered_agents():
    registry = AgentRegistry()
    a1 = make_agent(id="a1")
    a2 = make_agent(id="a2")
    registry.register(a1)
    registry.register(a2)
    assert registry.all() == [a1, a2]


def test_remove_agent():
    registry = AgentRegistry()
    agent = make_agent(id="to-remove")
    registry.register(agent)
    registry.remove("to-remove")
    assert registry.get("to-remove") is None


def test_remove_updates_name_index():
    registry = AgentRegistry()
    agent = make_agent(id="a1", name="RemoveMe")
    registry.register(agent)
    registry.remove("a1")
    assert registry.get_by_name("RemoveMe") is None


def test_remove_nonexistent_does_not_raise():
    registry = AgentRegistry()
    registry.remove("ghost")

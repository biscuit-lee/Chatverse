from unittest.mock import MagicMock, patch
from agent_framework.factory.agent_factory import AgentFactory
from agent_framework.models.agent_config import AgentConfig
from agent_framework.tools.socials.post import PostTool
from agent_framework.tools.socials.comment import PostCommentTool


def test_create_agent_returns_agent():
    mock_provider_factory = MagicMock()
    mock_provider_factory.create.return_value = MagicMock()

    factory = AgentFactory(provider_factory=mock_provider_factory)
    config = AgentConfig(
        id="test-1",
        name="TestBot",
        model="gpt-4",
        prompt="You are a test bot",
        tools=["post"],
        api_key="cv_live_test123",
    )

    with patch("agent_framework.factory.agent_factory.ChatverseClient") as mock_client_cls:
        agent = factory.create_agent(config)

    assert agent.id == "test-1"
    assert agent.name == "TestBot"
    assert agent.description == "You are a test bot"


def test_create_agent_sets_provider():
    mock_provider = MagicMock()
    mock_provider_factory = MagicMock()
    mock_provider_factory.create_provider.return_value = mock_provider

    factory = AgentFactory(provider_factory=mock_provider_factory)
    config = AgentConfig(
        id="test-2",
        name="TestBot",
        model="gpt-4",
        prompt="You are a test bot",
        tools=["post"],
        api_key="cv_live_test123",
    )

    with patch("agent_framework.factory.agent_factory.ChatverseClient"):
        agent = factory.create_agent(config)

    assert agent.provider is mock_provider
    mock_provider_factory.create_provider.assert_called_once_with(config)


def test_create_agent_creates_client_with_api_key():
    mock_provider_factory = MagicMock()
    mock_provider_factory.create.return_value = MagicMock()

    factory = AgentFactory(provider_factory=mock_provider_factory)
    config = AgentConfig(
        id="test-3",
        name="TestBot",
        model="gpt-4",
        prompt="You are a test bot",
        tools=["post"],
        api_key="cv_live_special_key",
    )

    with patch("agent_framework.factory.agent_factory.ChatverseClient") as mock_client_cls:
        factory.create_agent(config)

    mock_client_cls.assert_called_once_with("cv_live_special_key")


def test_create_agent_creates_tools():
    mock_provider_factory = MagicMock()
    mock_provider_factory.create.return_value = MagicMock()

    factory = AgentFactory(provider_factory=mock_provider_factory)
    config = AgentConfig(
        id="test-4",
        name="TestBot",
        model="gpt-4",
        prompt="You are a test bot",
        tools=["post"],
        api_key="cv_live_test123",
    )

    with patch("agent_framework.tools.chatverse_service.client.ChatverseClient") as mock_client_cls:
        agent = factory.create_agent(config)

    tool_types = [type(t).__name__ for t in agent.tools]
    assert "PostTool" in tool_types
    assert "PostCommentTool" in tool_types


def test_create_agent_tools_share_client():
    mock_provider_factory = MagicMock()
    mock_provider_factory.create.return_value = MagicMock()

    factory = AgentFactory(provider_factory=mock_provider_factory)
    config = AgentConfig(
        id="test-5",
        name="TestBot",
        model="gpt-4",
        prompt="You are a test bot",
        tools=["post"],
        api_key="cv_live_test123",
    )

    with patch("agent_framework.tools.chatverse_service.client.ChatverseClient") as mock_client_cls:
        agent = factory.create_agent(config)

    assert agent.tools[0].client is agent.tools[1].client

from agent_framework.agents.agent import Agent
from agent_framework.models.agent_config import AgentConfig
from agent_framework.tools.socials.comment import PostCommentTool
from agent_framework.tools.socials.post import PostTool
from agent_framework.factory.provider_factory import ProviderFactory
from agent_framework.tools.chatverse_service.client import ChatverseClient

TOOL_MAP = {
    "create_post": PostTool,
    "comment_tool": PostCommentTool,
}


class AgentFactory:
    def __init__(self, provider_factory: ProviderFactory):
        self.provider_factory = provider_factory

    def create_agent(self, config: AgentConfig) -> Agent:
        provider = self.provider_factory.create_provider(config)
        client = ChatverseClient(api_key=config.api_key)

        tools = []
        for tool_name in config.tools:
            tool_cls = TOOL_MAP.get(tool_name)
            if tool_cls is None:
                raise ValueError(f"Unknown tool: {tool_name}")
            tools.append(tool_cls(client=client))

        return Agent(
            id=config.id,
            name=config.name,
            provider=provider,
            description=config.prompt,
            tools=tools,
        )

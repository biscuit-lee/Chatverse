from agent_framework.providers.base_provider import BaseProvider
from agent_framework.tools.base_tool import BaseTool

class Agent:
    def __init__(self, name: str, description: str, tools: list[BaseTool], provider: BaseProvider):
        self.name = name
        self.description = description
        self.tools = tools
        self.provider = provider

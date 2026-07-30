from agent_framework.providers.base_provider import BaseProvider
from agent_framework.tools.base_tool import BaseTool
from agent_framework.tools.tool_registry import ToolRegistry

class Agent:
    def __init__(self, id:int, name: str, description: str, tools: list[BaseTool], provider: BaseProvider):
        self.id = id
        self.name = name
        self.description = description
        self.tools = tools
        self.provider = provider
        
        self.tool_registry = ToolRegistry()

        for tool in tools:
            self.tool_registry.register(tool)
    

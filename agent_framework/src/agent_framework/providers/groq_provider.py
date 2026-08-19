from agent_framework.providers.base_provider import BaseProvider
from agent_framework.tools.base_tool import BaseTool
from groq import Groq
from agent_framework.config.settings import settings

class GroqProvider(BaseProvider):
    def __init__(self, model: str):
        super().__init__()
        self.model = model
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate(self, messages: list[dict], tools: list[BaseTool] = None):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.format_tools(tools),
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            stream=False,
            stop=None
        )

        return completion.choices[0].message

    """
    Format a list of tools into the required structure for the Groq API.

    """
    @staticmethod
    def format_tools(tools: list[BaseTool]) -> list[dict]:
        if tools is None:
            return []

        formatted_tools = []
        for tool in tools:
            formatted_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.argument_schema()
                    }
            }
            formatted_tools.append(formatted_tool)
        return formatted_tools

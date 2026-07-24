from agent_framework.providers.base_provider import BaseProvider
from agent_framework.tools.base_tool import BaseTool
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqProvider(BaseProvider):
    def __init__(self, model: str):
        super().__init__()
        self.model = model

    def generate(self, messages: list[dict], tools: list[dict] = None):
        client = Groq()
        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools if tools is not None else [],
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
            stop=None
        )

        return completion.choices[0].message

    @staticmethod
    def format_tools(tools: list[BaseTool]) -> list[dict]:
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

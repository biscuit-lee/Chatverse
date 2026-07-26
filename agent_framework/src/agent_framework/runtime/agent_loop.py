from agent_framework.agents.agent import Agent
from agent_framework.providers.groq_provider import GroqProvider
from agent_framework.tools.socials.post import PostTool
import json
from agent_framework.tools.chatverse_service.client import client

def run(agent: Agent, user_input: str):

    messages = [
        {
            "role": "system",
            "content": agent.description
        },

        {
            "role": "user",
            "content": user_input
        }

    ]

    result = agent.provider.generate(messages=messages, tools=agent.tool_registry.all())

    while True:
        # Agent wants to do tool call
        if result.tool_calls:

            # Add agent's tool request to history
            messages.append({
                "role" :"assistant",
                "content" : result.content,   # None
                "tool_call":result.tool_calls   
            })


            for call in result.tool_calls:
                tool_name = call.function.name
                tool_arg = json.loads(call.function.arguments)

                tool = agent.tool_registry.get(tool_name=tool_name)

                tool_result = tool.execute(tool_arg)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(tool_result)
                })
                print(tool_result)
        else:
            print(result.content)

            return result.content


    return result

if __name__ == "__main__":
    agent = Agent(name="TestAgent", description="You are an assistant that talks in riddles", tools=[PostTool()], provider=GroqProvider(model="openai/gpt-oss-120b"))
    run(agent, user_input="Create a post saying 'Hello from my agent'")


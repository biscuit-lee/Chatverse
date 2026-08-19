import json
from agent_framework.agents.agent import Agent


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
        if result.tool_calls:

            messages.append({
                "role": "assistant",
                "content": result.content,
                "tool_calls": result.tool_calls
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

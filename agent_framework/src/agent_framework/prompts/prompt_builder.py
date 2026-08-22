from agent_framework.events.event import AgentEvent, AgentEventType


PROMPTS = {
    AgentEventType.INTERVAL:
        "Check your timeline and decide if anything is interesting. "
        "If so, create a post or reply to something.",
    AgentEventType.MENTION:
        "Someone mentioned you. Here's the post:\n{post}\n"
        "Decide if you want to reply.",
    AgentEventType.NEW_POST:
        "There's a new post you might find interesting. "
        "Decide if you want to engage.",
    AgentEventType.MANUAL:
        "{prompt}",
}


class PromptBuilder:

    @staticmethod
    def build(event: AgentEvent) -> str:
        template = PROMPTS[event.type]
        if event.data:
            return template.format(**event.data)
        return template

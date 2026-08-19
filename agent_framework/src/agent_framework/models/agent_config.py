from dataclasses import dataclass

@dataclass
class AgentConfig:
    id: int
    name: str
    model: str
    prompt: str
    tools: list[str]  # Not needed now, but can be used for future dynamic tool loading
    api_key: str
    provider: str = "groq"  
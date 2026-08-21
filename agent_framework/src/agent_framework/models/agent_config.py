from dataclasses import dataclass

@dataclass
class AgentConfig:
    id: int
    name: str
    model: str
    prompt: str
    tools: list[str]
    api_key: str
    provider: str = "groq"
    interval: int = 0
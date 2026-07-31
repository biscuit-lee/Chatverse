from agent_framework.providers.base_provider import BaseProvider

class ProviderRegistry:

    """
    Stores available providers CLASS TYPES and allows for their registration and retrieval by name.
    """

    def __init__(self):
        self.providers: dict[str, type[BaseProvider]] = {}

    def register(self, name: str, provider: type[BaseProvider]):
        if name in self.providers:
            raise ValueError(f"Provider '{name}' is already registered.")
        self.providers[name] = provider

    def get(self, name: str) -> type[BaseProvider]:
        return self.providers.get(name)
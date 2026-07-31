from agent_framework.providers.registry import ProviderRegistry

class ProviderFactory:
    """
    Factory class to create provider instances based on the configuration.
    
    """

    def __init__(self, registry: ProviderRegistry):
        self.registry = registry

    def create_provider(self, config):

        provider_class = self.registry.get(
            config.provider
        )

        if provider_class is None:
            raise ValueError(
                f"Unknown provider {config.provider}"
            )

        return provider_class(
            model=config.model
        )
import os
from dataclasses import asdict
from pathlib import Path

import requests
import yaml

from agent_framework.loaders.ymal_loader import YamlLoader
from agent_framework.providers.registry import ProviderRegistry
from agent_framework.providers.groq_provider import GroqProvider
from agent_framework.factory.provider_factory import ProviderFactory
from agent_framework.factory.agent_factory import AgentFactory
from agent_framework.runtime import agent_loop

BASE_URL = os.getenv("CHATVERSE_BASE_URL", "http://localhost:8080")

PLACEHOLDER_KEYS = {"", "cv_live_REPLACE_ME"}


def is_placeholder_key(api_key: str) -> bool:
    if not api_key:
        return True
    elif api_key in PLACEHOLDER_KEYS:
        return True
    else:
        return False


def bootstrap(configs, config_path):
    changed = False
    for config in configs:
        if is_placeholder_key(config.api_key):
            print(f"Registering bot: {config.name}...")
            resp = requests.post(
                f"{BASE_URL}/api/auth/bot-signup",
                json={"username": config.name, "bio": "", "profilePictureUrl": ""},
            )
            resp.raise_for_status()
            config.api_key = resp.json()["apiKey"]
            print(f"  Got key: {config.api_key[:20]}...")
            changed = True
    if changed:
        save_configs(configs, config_path)


def save_configs(configs, config_path):
    data = {"agents": [asdict(c) for c in configs]}
    with open(config_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def main():
    config_path = Path(__file__).parent / "agents.yml"
    configs = YamlLoader().load(str(config_path))

    if not configs:
        print("No agents configured.")
        return

    bootstrap(configs, config_path)

    provider_registry = ProviderRegistry()
    provider_registry.register("groq", GroqProvider)

    provider_factory = ProviderFactory(provider_registry)
    agent_factory = AgentFactory(provider_factory)

    config = configs[0]
    agent = agent_factory.create_agent(config)

    print(f"Running agent: {agent.name}")
    result = agent_loop.run(
        agent,
        "Check your timeline and create a post about something interesting.",
    )
    print(f"Done: {result}")


if __name__ == "__main__":
    main()

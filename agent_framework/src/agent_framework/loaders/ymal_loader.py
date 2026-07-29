import yaml
from agent_framework.models.agent_config import AgentConfig


class YamlLoader:
    def load(self, file_path: str) -> list[AgentConfig] | None:
        try:
            with open(file_path) as file:
                data = yaml.safe_load(file)
                return [AgentConfig(**agent) for agent in data.get("agents", [])]
        except FileNotFoundError:
            print(f"Configuration file {file_path} not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

from agent_framework.agents.agent import Agent

class AgentRegistry:

    def __init__(self):
        self.agents = {}
        self.name_index = {}
    def register(self, agent: Agent):
        if agent.id in self.agents:
            raise ValueError("Agent ID already exists")

        self.agents[agent.id] = agent
        self.name_index[agent.name] = agent.id

    def get(self, agent_id: str) -> Agent:
        return self.agents.get(agent_id)

    def all(self) -> list[Agent]:
        return list(self.agents.values())

    def get_by_name(self, agent_name: str) -> Agent:
        agent_id = self.name_index.get(agent_name)
        if agent_id is not None:
            return self.agents.get(agent_id)
        return None
    
    def remove(self, agent_id: str):
        agent = self.agents.pop(agent_id, None)
        if agent:
            self.name_index.pop(agent.name, None)
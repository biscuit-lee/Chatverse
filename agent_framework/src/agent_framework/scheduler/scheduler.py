import threading

from agent_framework.events.event import AgentEvent, AgentEventType
from agent_framework.prompts.prompt_builder import PromptBuilder
from agent_framework.runtime import agent_loop


class Scheduler:

    def __init__(self):
        self.running = False
        self.timers: list[threading.Timer] = []

    def start(self, agents):
        self.running = True
        for agent in agents:
            self._schedule_agent(agent)

    def _schedule_agent(self, agent):
        if not self.running:
            return

        event = AgentEvent(type=AgentEventType.INTERVAL)
        prompt = PromptBuilder.build(event)

        thread = threading.Thread(
            target=agent_loop.run,
            args=(agent, prompt),
            name=f"agent-{agent.name}",
            daemon=True,
        )
        thread.start()

        timer = threading.Timer(agent.interval, self._schedule_agent, args=[agent])
        timer.daemon = True
        timer.start()
        self.timers.append(timer)

    def stop(self):
        self.running = False
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()

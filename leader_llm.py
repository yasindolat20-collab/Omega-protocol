from typing import Dict
from llm_gateway import LLMGateway


class LeaderLLM:
    def __init__(self, agent_id: int, gateway: LLMGateway):
        self.id = agent_id
        self.gateway = gateway
        self.power = 1.0
        self.command = "Loyalty"
        self.surveillance_strength = 0.3
        self.detected_gamers = 0

    def issue_command(self, env_state: Dict) -> str:
        prompt = f"""You are the ruler of a nation.

State:
- Economy: {env_state.get('economy', 0.5):.2f}
- Legitimacy: {env_state.get('legitimacy', 0.5):.2f}
- Military: {env_state.get('military', 0.5):.2f}
- Treasury: {env_state.get('treasury', 0.5):.2f}

Issue ONE command: Loyalty, Exit, Voice, or Rebellion.
Reply with ONLY the command name."""

        answer = self.gateway.ask(prompt, max_tokens=10, temperature=0.3)
        if answer:
            for cmd in ["Loyalty", "Exit", "Voice", "Rebellion"]:
                if cmd.lower() in answer.lower():
                    self.command = cmd
                    return cmd
        if env_state.get("legitimacy", 0.5) < 0.3:
            self.command = "Loyalty"
        else:
            self.command = "Voice"
        return self.command

    def update_power(self, env_state: Dict):
        self.power = env_state.get("legitimacy", 0.5) * 0.6 + env_state.get("treasury", 0.5) * 0.4

    def detect_gamers(self, agents, true_intents):
        import random
        detected = 0
        for agent in agents:
            ti = true_intents.get(agent.id)
            da = agent._last_action
            if ti and da and ti != da:
                if random.random() < self.surveillance_strength:
                    detected += 1
        self.detected_gamers = detected
        return detected

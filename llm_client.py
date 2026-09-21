from typing import Dict, List
from llm_gateway import LLMGateway


class LLMClient:
    def __init__(self, gateway: LLMGateway = None):
        self.gateway = gateway if gateway else LLMGateway()
        self.cache = {}
        self.cache_hits = 0
        self.calls = 0

    def get_agent_decision(self, agent_info: Dict, env_state: Dict, allowed_actions: List[str]) -> str:
        cache_key = (
            agent_info["archetype"],
            agent_info["goal"],
            round(env_state.get("economy", 0.5), 1),
            round(env_state.get("legitimacy", 0.5), 1),
            round(env_state.get("military", 0.5), 1),
            round(env_state.get("treasury", 0.5), 1),
            round(agent_info["risk_aversion"], 1),
        )
        if cache_key in self.cache:
            self.cache_hits += 1
            return self.cache[cache_key]

        prompt = f"""You are an agent in a socio-political simulation.

Identity: {agent_info['archetype']}
Goal: {agent_info['goal']}
Risk aversion: {agent_info['risk_aversion']:.2f}

Environment:
- Economy: {env_state.get('economy', 0.5):.2f}
- Legitimacy: {env_state.get('legitimacy', 0.5):.2f}
- Military: {env_state.get('military', 0.5):.2f}
- Treasury: {env_state.get('treasury', 0.5):.2f}

Recent memory: {agent_info.get('memory', [])}

Choose ONE action from: {allowed_actions}
Reply with ONLY the action name, nothing else."""

        self.calls += 1
        answer = self.gateway.ask(prompt, max_tokens=10, temperature=0.5)

        result = allowed_actions[0]
        if answer:
            for valid in allowed_actions:
                if valid.lower() in answer.lower():
                    result = valid
                    break

        self.cache[cache_key] = result
        return result

    def stats(self) -> Dict:
        return {
            "calls": self.calls,
            "cache_hits": self.cache_hits,
            "cache_size": len(self.cache),
            "gateway": self.gateway.get_stats(),
        }

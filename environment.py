import random
from typing import Dict, List

class Environment:
    def __init__(self):
        self.economy = 0.5
        self.legitimacy = 0.5
        self.military = 0.5
        self.treasury = 0.5

    def _clamp(self, value):
        return max(0.0, min(1.0, value))

    def get_state(self):
        return {"economy": self.economy, "legitimacy": self.legitimacy,
                "military": self.military, "treasury": self.treasury}

    def shock(self):
        if random.random() < 0.10:
            t = random.choice(["war", "famine", "crisis"])
            if t == "war":
                self.military = self._clamp(self.military - 0.15)
            elif t == "famine":
                self.economy = self._clamp(self.economy - 0.15)
            elif t == "crisis":
                self.legitimacy = self._clamp(self.legitimacy - 0.15)
            return t
        return None

    def step(self, agent_actions):
        n = len(agent_actions) if agent_actions else 1
        loyalty = agent_actions.count("Loyalty")
        exit_count = agent_actions.count("Exit")
        voice = agent_actions.count("Voice")
        rebellion = agent_actions.count("Rebellion")
        self.treasury -= 0.06 * (loyalty / n)
        self.treasury += 0.02 * (exit_count / n)
        self.economy -= 0.02 * (exit_count / n) + 0.01 * (rebellion / n)
        self.economy += 0.01 * (loyalty / n) + 0.005 * (voice / n)
        self.legitimacy += 0.02 * (loyalty / n) - 0.04 * (rebellion / n) + 0.01 * (voice / n)
        self.military -= 0.02 * (exit_count / n) - 0.01 * (rebellion / n) + 0.005 * (loyalty / n)
        self.economy = self._clamp(self.economy)
        self.legitimacy = self._clamp(self.legitimacy)
        self.military = self._clamp(self.military)
        self.treasury = self._clamp(self.treasury)
        outcome = {
            "Loyalty": self.treasury > 0.2 and self.legitimacy > 0.4,
            "Exit": self.economy < 0.5,
            "Voice": self.legitimacy > 0.4,
            "Rebellion": self.legitimacy < 0.3 and self.military < 0.5,
        }
        return {"outcome": outcome, "state": self.get_state(),
                "counts": {"Loyalty": loyalty, "Exit": exit_count,
                           "Voice": voice, "Rebellion": rebellion}}

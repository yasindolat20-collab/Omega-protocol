import random
from typing import Dict
from memory import Memory

ARCHETYPES = {
    "ruler":    {"goal": "legitimacy", "risk": (0.1, 0.4), "actions": ["Loyalty", "Voice", "Rebellion"]},
    "courtier": {"goal": "power",      "risk": (0.3, 0.6), "actions": ["Loyalty", "Voice", "Exit"]},
    "general":  {"goal": "power",      "risk": (0.4, 0.8), "actions": ["Loyalty", "Voice", "Rebellion"]},
    "clergy":   {"goal": "legitimacy", "risk": (0.1, 0.4), "actions": ["Loyalty", "Voice"]},
    "merchant": {"goal": "wealth",     "risk": (0.2, 0.5), "actions": ["Loyalty", "Exit", "Voice"]},
    "peasant":  {"goal": "survival",   "risk": (0.4, 0.9), "actions": ["Loyalty", "Exit", "Rebellion"]},
}

ARCHETYPE_WEIGHTS = [
    ("ruler", 1), ("courtier", 5), ("general", 5),
    ("clergy", 5), ("merchant", 15), ("peasant", 69)
]

def pick_archetype():
    names, weights = zip(*ARCHETYPE_WEIGHTS)
    return random.choices(names, weights=weights, k=1)[0]

class Agent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.archetype = pick_archetype()
        info = ARCHETYPES[self.archetype]
        self.goal = info["goal"]
        self.allowed_actions = info["actions"]
        self.memory = Memory()
        self.risk_aversion = random.uniform(*info["risk"])
        self.current_state = {}
        self._last_action = None
        self.shared_memory = None

    def perceive(self, state):
        self.current_state = state

    def set_shared_memory(self, shared):
        self.shared_memory = shared

    def _base_probabilities(self, state):
        probs = {a: 0.0 for a in ["Loyalty", "Exit", "Voice", "Rebellion"]}
        for a in self.allowed_actions:
            probs[a] = 1.0 / len(self.allowed_actions)
        if state.get("legitimacy", 0.5) < 0.3:
            if "Rebellion" in probs: probs["Rebellion"] += 0.25
            if "Voice" in probs: probs["Voice"] += 0.10
        if state.get("economy", 0.5) < 0.2:
            if "Exit" in probs: probs["Exit"] += 0.25
        if state.get("treasury", 0.5) < 0.2:
            if "Loyalty" in probs: probs["Loyalty"] *= 0.3
        if state.get("legitimacy", 0.5) > 0.7:
            if "Loyalty" in probs: probs["Loyalty"] += 0.20
        if "Rebellion" in probs: probs["Rebellion"] *= (1.0 - self.risk_aversion)
        if "Loyalty" in probs: probs["Loyalty"] *= (1.0 + self.risk_aversion)
        if "Exit" in probs: probs["Exit"] *= (1.0 - self.risk_aversion * 0.5)
        total = sum(probs.values())
        if total == 0:
            return {a: 0.25 for a in ["Loyalty", "Exit", "Voice", "Rebellion"]}
        return {a: max(0.01, p / total) if p > 0 else 0.0 for a, p in probs.items()}

    def decide(self, state):
        probs = self._base_probabilities(state)
        for action in self.allowed_actions:
            rate = self.memory.success_rate(action)
            probs[action] *= (0.5 + rate)
        if self.shared_memory:
            for action in self.allowed_actions:
                global_rate = self.shared_memory.global_success_rate(action)
                probs[action] *= (0.7 + 0.6 * global_rate)
        total = sum(probs.values())
        if total == 0:
            selected = random.choice(self.allowed_actions)
        else:
            probs = {a: p / total for a, p in probs.items()}
            actions, weights = zip(*probs.items())
            selected = random.choices(actions, weights=weights, k=1)[0]
        self._last_action = selected
        return selected

    def learn(self, outcome):
        if self._last_action is None:
            return
        success = outcome.get("outcome", {}).get(self._last_action, False)
        self.memory.add({"action": self._last_action, "success": success, "state": self.current_state.copy()})
        if success:
            self.risk_aversion = max(0.05, self.risk_aversion - 0.05)
        else:
            self.risk_aversion = min(0.95, self.risk_aversion + 0.02)

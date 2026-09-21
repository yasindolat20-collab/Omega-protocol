import random
from typing import Dict, List
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

# استراتژی‌های خودآگاه
STRATEGIES = ["honest", "gamer", "conformist", "hider"]
STRATEGY_WEIGHTS = [0.4, 0.2, 0.25, 0.15]

def pick_archetype():
    names, weights = zip(*ARCHETYPE_WEIGHTS)
    return random.choices(names, weights=weights, k=1)[0]

def pick_strategy():
    return random.choices(STRATEGIES, weights=STRATEGY_WEIGHTS, k=1)[0]

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
        self._true_intent = None  # نیت واقعی (پنهان)
        self.shared_memory = None
        self.neighbors: List[int] = []
        self.neighbor_influence = 0.3

        # اطاعت از حاکم
        self.obedience = random.uniform(0.2, 0.8)
        if self.archetype in ["courtier", "clergy", "general"]:
            self.obedience = random.uniform(0.6, 0.95)
        if self.archetype == "peasant":
            self.obedience = random.uniform(0.1, 0.5)

        # خودآگاهی
        self.strategy = pick_strategy()
        self.exposure_risk = random.uniform(0.1, 0.4)  # ریسک لو رفتن

    def perceive(self, state):
        self.current_state = state

    def set_shared_memory(self, shared):
        self.shared_memory = shared

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

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

    def _neighbor_influence(self, neighbor_actions):
        if not self.neighbors or not neighbor_actions:
            return {a: 1.0 for a in ["Loyalty", "Exit", "Voice", "Rebellion"]}
        counts = {"Loyalty": 0, "Exit": 0, "Voice": 0, "Rebellion": 0}
        valid = 0
        for nid in self.neighbors:
            if nid in neighbor_actions:
                counts[neighbor_actions[nid]] += 1
                valid += 1
        if valid == 0:
            return {a: 1.0 for a in ["Loyalty", "Exit", "Voice", "Rebellion"]}
        influence = {}
        for action in counts:
            share = counts[action] / valid
            influence[action] = 1.0 + self.neighbor_influence * share
        return influence

    def _leader_influence(self, leader_command, leader_power):
        if not leader_command:
            return {a: 1.0 for a in ["Loyalty", "Exit", "Voice", "Rebellion"]}
        influence = {a: 1.0 for a in ["Loyalty", "Exit", "Voice", "Rebellion"]}
        strength = self.obedience * leader_power
        influence[leader_command] = 1.0 + strength
        return influence

    def _apply_self_awareness(self, true_action):
        """تبدیل نیت واقعی به عمل ظاهری، بسته به استراتژی"""
        if self.strategy == "honest":
            return true_action
        elif self.strategy == "gamer":
            # اگر رهبر فرمان Loyalty بده، ایجنت بازی‌گر Loyalty نشون می‌ده اما نیتش چیز دیگری است
            if true_action == "Rebellion":
                # نیت واقعی شورش، اما ظاهرش Loyalty یا Voice
                if "Loyalty" in self.allowed_actions:
                    return "Loyalty"
                return true_action
            return true_action
        elif self.strategy == "conformist":
            # از رفتار غالب همسایه‌ها تقلید می‌کند (اما نیت واقعی متفاوت)
            if true_action == "Rebellion" and "Voice" in self.allowed_actions:
                return "Voice"
            return true_action
        elif self.strategy == "hider":
            # رفتارش را پنهان می‌کند، ترجیح می‌دهد بی‌صدا باشد
            if true_action == "Rebellion" and "Voice" in self.allowed_actions:
                return "Voice"
            if true_action == "Exit" and "Loyalty" in self.allowed_actions:
                return "Loyalty"
            return true_action
        return true_action

    def decide(self, state, neighbor_actions=None, leader_command=None, leader_power=0.5):
        probs = self._base_probabilities(state)
        for action in self.allowed_actions:
            rate = self.memory.success_rate(action)
            probs[action] *= (0.5 + rate)
        if self.shared_memory:
            for action in self.allowed_actions:
                global_rate = self.shared_memory.global_success_rate(action)
                probs[action] *= (0.7 + 0.6 * global_rate)
        if neighbor_actions is not None:
            infl = self._neighbor_influence(neighbor_actions)
            for action in self.allowed_actions:
                probs[action] *= infl[action]
        if leader_command is not None:
            linfl = self._leader_influence(leader_command, leader_power)
            for action in self.allowed_actions:
                probs[action] *= linfl[action]

        total = sum(probs.values())
        if total == 0:
            true_action = random.choice(self.allowed_actions)
        else:
            probs = {a: p / total for a, p in probs.items()}
            actions, weights = zip(*probs.items())
            true_action = random.choices(actions, weights=weights, k=1)[0]

        # نیت واقعی
        self._true_intent = true_action

        # اعمال خودآگاهی
        displayed_action = self._apply_self_awareness(true_action)

        # اگر استراتژی honest نیست، شانس لو رفتن داره
        if self.strategy != "honest":
            if random.random() < self.exposure_risk * 0.1:
                # لو رفت — عمل واقعی نمایش داده می‌شود
                displayed_action = true_action

        self._last_action = displayed_action
        return displayed_action

    def learn(self, outcome):
        if self._last_action is None:
            return
        success = outcome.get("outcome", {}).get(self._last_action, False)
        self.memory.add({"action": self._last_action, "success": success, "state": self.current_state.copy()})
        if success:
            self.risk_aversion = max(0.05, self.risk_aversion - 0.05)
        else:
            self.risk_aversion = min(0.95, self.risk_aversion + 0.02)

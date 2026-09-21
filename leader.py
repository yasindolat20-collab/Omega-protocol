import random
from typing import Dict, List

class Leader:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.power = 1.0
        self.command = None
        self.surveillance_strength = 0.3  # قدرت رصد (0 تا 1)
        self.detected_gamers = 0
        self.detected_hiders = 0

    def issue_command(self, env_state: Dict) -> str:
        legitimacy = env_state.get("legitimacy", 0.5)
        economy = env_state.get("economy", 0.5)
        military = env_state.get("military", 0.5)
        treasury = env_state.get("treasury", 0.5)
        if legitimacy < 0.3:
            self.command = "Loyalty"
        elif economy < 0.3:
            self.command = "Voice"
        elif military < 0.3:
            self.command = "Loyalty"
        elif treasury < 0.2:
            self.command = "Exit"
        else:
            self.command = "Loyalty"
        return self.command

    def update_power(self, env_state: Dict):
        legitimacy = env_state.get("legitimacy", 0.5)
        treasury = env_state.get("treasury", 0.5)
        self.power = (legitimacy * 0.6 + treasury * 0.4)

    def detect_gamers(self, agents, true_intents):
        """رصد ایجنت‌های بازی‌گر — فقط اونایی که استراتژی‌شون gamer یا hider هست"""
        detected = 0
        for agent in agents:
            true_intent = true_intents.get(agent.id)
            displayed = agent._last_action
            if true_intent and displayed:
                if true_intent != displayed:
                    # تفاوت بین نیت و نمایش — یعنی پنهان‌کار یا بازی‌گر
                    if random.random() < self.surveillance_strength:
                        detected += 1
        self.detected_gamers = detected
        return detected

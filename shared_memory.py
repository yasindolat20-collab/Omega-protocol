from typing import Dict, List, Any
from collections import defaultdict

class SharedMemory:
    def __init__(self, decay=0.95):
        self.experiences = []
        self.action_success = defaultdict(list)
        self.decay = decay  # هر تجربه در هر گام، وزنش ضرب در decay می‌شود

    def add(self, agent_id, action, success, state):
        exp = {"agent_id": agent_id, "action": action, "success": success, "state": state.copy()}
        self.experiences.append(exp)
        self.action_success[action].append(success)
        if len(self.experiences) > 10000:
            self.experiences = self.experiences[-10000:]
            self.action_success[action] = self.action_success[action][-2000:]

    def global_success_rate(self, action, window=500):
        # فقط تجربه‌های اخیر را می‌بینیم (فراموشی)
        rates = self.action_success.get(action, [])
        if not rates:
            return 0.5
        recent = rates[-window:]
        return sum(recent) / len(recent)

    def decay_old(self):
        # پاک کردن تجربه‌های خیلی قدیمی به صورت دوره‌ای
        if len(self.experiences) > 2000:
            keep = int(len(self.experiences) * 0.5)
            self.experiences = self.experiences[-keep:]
            for action in list(self.action_success.keys()):
                self.action_success[action] = self.action_success[action][-keep:]

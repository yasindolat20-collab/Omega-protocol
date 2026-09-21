import random
from typing import Dict, List

class Leader:
    """حاکم مرکزی که می‌تواند فرمان دهد و منابع توزیع کند"""

    def __init__(self, agent_id: int):
        self.id = agent_id
        self.power = 1.0  # قدرت فرمان‌دهی (0 تا 1)
        self.command = None  # فرمان فعلی
        self.command_strength = 0.5  # قدرت تأثیر فرمان

    def issue_command(self, env_state: Dict, followers_mood: Dict) -> str:
        """بر اساس وضعیت، فرمان می‌دهد"""
        legitimacy = env_state.get("legitimacy", 0.5)
        economy = env_state.get("economy", 0.5)
        military = env_state.get("military", 0.5)
        treasury = env_state.get("treasury", 0.5)

        # منطق فرمان‌دهی
        if legitimacy < 0.3:
            self.command = "Loyalty"  # در بحران مشروعیت: درخواست وفاداری
        elif economy < 0.3:
            self.command = "Voice"  # در بحران اقتصادی: درخواست اعتراض مسالمت‌آمیز
        elif military < 0.3:
            self.command = "Loyalty"  # در بحران نظامی: درخواست وفاداری
        elif treasury < 0.2:
            self.command = "Exit"  # در بحران مالی: اجازه خروج
        else:
            self.command = "Loyalty"  # حالت عادی: وفاداری

        return self.command

    def update_power(self, env_state: Dict):
        """قدرت حاکم بر اساس وضعیت به‌روز می‌شود"""
        legitimacy = env_state.get("legitimacy", 0.5)
        treasury = env_state.get("treasury", 0.5)
        # قدرت = ترکیب مشروعیت و خزانه
        self.power = (legitimacy * 0.6 + treasury * 0.4)

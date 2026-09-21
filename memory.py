from typing import Any, Dict, List

class Memory(list):
    def add(self, experience: Dict[str, Any]) -> None:
        self.append(experience)
    def recall(self, last_n: int = 5) -> List[Dict[str, Any]]:
        return self[-last_n:] if last_n > 0 else []
    def success_rate(self, action: str) -> float:
        relevant = [e for e in self if e.get("action") == action]
        if not relevant:
            return 0.5
        successes = sum(1 for e in relevant if e.get("success"))
        return successes / len(relevant)

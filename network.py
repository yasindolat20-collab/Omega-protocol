import random
from typing import Dict, List

class SocialNetwork:
    def __init__(self, n_agents: int, k: int = 4, p: float = 0.1):
        self.n = n_agents
        self.k = k
        self.p = p
        self.adjacency: Dict[int, List[int]] = {}
        self._build()

    def _build(self):
        for i in range(self.n):
            self.adjacency[i] = []
            for j in range(1, self.k // 2 + 1):
                self.adjacency[i].append((i + j) % self.n)
                self.adjacency[i].append((i - j) % self.n)
        for i in range(self.n):
            for idx, neighbor in enumerate(self.adjacency[i]):
                if random.random() < self.p:
                    new_neighbor = random.randint(0, self.n - 1)
                    if new_neighbor != i and new_neighbor not in self.adjacency[i]:
                        self.adjacency[i][idx] = new_neighbor
                        if i not in self.adjacency[new_neighbor]:
                            self.adjacency[new_neighbor].append(i)

    def neighbors_of(self, agent_id: int) -> List[int]:
        return self.adjacency.get(agent_id, [])

    def stats(self) -> Dict:
        degrees = [len(v) for v in self.adjacency.values()]
        return {
            "n": self.n,
            "avg_degree": sum(degrees) / len(degrees),
            "min_degree": min(degrees),
            "max_degree": max(degrees),
        }

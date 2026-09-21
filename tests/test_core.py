import pytest

from agent import Agent
from environment import Environment
from memory import Memory
from network import SocialNetwork
from shared_memory import SharedMemory


def test_environment_initial():
    env = Environment()
    state = env.get_state()
    assert state == {"economy": 0.5, "legitimacy": 0.5, "military": 0.5, "treasury": 0.5}


def test_environment_step():
    env = Environment()
    result = env.step(["Loyalty", "Loyalty", "Voice", "Exit"])
    assert set(result.keys()) == {"outcome", "state", "counts"}
    assert result["counts"] == {"Loyalty": 2, "Exit": 1, "Voice": 1, "Rebellion": 0}
    for key in ["economy", "legitimacy", "military", "treasury"]:
        assert 0.0 <= result["state"][key] <= 1.0


def test_environment_clamping():
    env = Environment()
    env.economy = 1.0
    env.legitimacy = 1.0
    env.military = 1.0
    env.treasury = 1.0
    result = env.step(["Rebellion", "Rebellion", "Rebellion"])
    state = result["state"]
    assert all(0.0 <= state[k] <= 1.0 for k in state)


def test_memory_basic():
    mem = Memory()
    mem.add({"action": "Loyalty", "success": True})
    mem.add({"action": "Exit", "success": False})
    assert len(mem) == 2
    assert mem.recall(1)[0]["action"] == "Exit"
    assert mem.success_rate("Loyalty") == 1.0
    assert mem.success_rate("Unknown") == 0.5


def test_shared_memory():
    shared = SharedMemory(decay=0.95)
    shared.add(1, "Loyalty", True, {"economy": 0.6})
    shared.add(2, "Exit", False, {"economy": 0.2})
    assert len(shared.experiences) == 2
    assert shared.global_success_rate("Loyalty") == 1.0
    assert shared.global_success_rate("Unknown") == 0.5


def test_agent_decide():
    agent = Agent(1, use_llm=False)
    agent.perceive({"economy": 0.2, "legitimacy": 0.2, "military": 0.5, "treasury": 0.1})
    action = agent.decide({"economy": 0.2, "legitimacy": 0.2, "military": 0.5, "treasury": 0.1}, neighbor_actions={}, leader_command="Loyalty", leader_power=0.8)
    assert action in agent.allowed_actions
    assert action in {"Loyalty", "Exit", "Voice", "Rebellion"}


def test_network():
    network = SocialNetwork(20, k=4, p=0.0)
    assert len(network.adjacency) == 20
    for idx, neighbors in network.adjacency.items():
        assert idx not in neighbors
        assert len(neighbors) > 0
        assert all(0 <= n < 20 for n in neighbors)

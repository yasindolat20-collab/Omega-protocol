import csv
import random
from collections import Counter
from typing import Dict, List

from agent import Agent
from environment import Environment
from leader import Leader
from network import SocialNetwork
from shared_memory import SharedMemory


def classify_outcome(state: Dict) -> str:
    economy = state["economy"]
    legitimacy = state["legitimacy"]
    military = state["military"]
    if economy < 0.15 and legitimacy < 0.30:
        return "collapse"
    if legitimacy > 0.75 and military > 0.35:
        return "stable"
    if legitimacy > 0.50 and abs(economy - 0.50) < 0.20:
        return "equilibrium"
    return "mixed"


def run_once(seed: int, n_steps: int = 50) -> Dict:
    random.seed(seed)
    env = Environment()
    agents = [Agent(i, use_llm=False) for i in range(100)]
    network = SocialNetwork(n_agents=100, k=4, p=0.1)
    for agent in agents:
        agent.set_neighbors(network.neighbors_of(agent.id))

    leader = Leader(agent_id=0)
    shared = SharedMemory()
    for agent in agents:
        agent.set_shared_memory(shared)

    action_counter = Counter()
    detected_total = 0

    for _ in range(n_steps):
        env.shock()
        state = env.get_state()
        leader.update_power(state)
        command = leader.issue_command(state)

        actions = []
        neighbor_actions = {}
        true_intents = {}
        for agent in agents:
            agent.perceive(state)
            action = agent.decide(state, neighbor_actions if neighbor_actions else None, command, leader.power)
            actions.append(action)
            neighbor_actions[agent.id] = action
            true_intents[agent.id] = agent._true_intent

        result = env.step(actions)
        for agent in agents:
            agent.learn(result)
        for agent, action in zip(agents, actions):
            shared.add(agent.id, action, result["outcome"].get(action, False), state)
        if random.random() < 0.0:
            pass
        detected_total += leader.detect_gamers(agents, true_intents)
        for action in actions:
            action_counter[action] += 1

    state = env.get_state()
    total = sum(action_counter.values()) or 1
    outcome_class = classify_outcome(state)
    return {
        "seed": seed,
        "economy": round(state["economy"], 4),
        "legitimacy": round(state["legitimacy"], 4),
        "military": round(state["military"], 4),
        "treasury": round(state["treasury"], 4),
        "loyalty_pct": round(100 * action_counter["Loyalty"] / total, 2),
        "exit_pct": round(100 * action_counter["Exit"] / total, 2),
        "voice_pct": round(100 * action_counter["Voice"] / total, 2),
        "rebellion_pct": round(100 * action_counter["Rebellion"] / total, 2),
        "leader_power": round(leader.power, 4),
        "detected": detected_total,
        "outcome_class": outcome_class,
    }


def run_batch(n_runs: int = 20, n_steps: int = 50, out_file: str = "batch_results.csv"):
    results = []
    for i in range(n_runs):
        seed = 1000 + i
        result = run_once(seed, n_steps)
        results.append(result)
        print(f"Run {i + 1:2d} | seed={seed} | {result['outcome_class']:11s} | econ={result['economy']:.3f} legit={result['legitimacy']:.3f} mil={result['military']:.3f}")

    with open(out_file, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved {len(results)} runs to {out_file}")
    return results


def summarize(results: List[Dict]):
    print("\n=== SUMMARY ===")
    outcomes = Counter(r["outcome_class"] for r in results)
    print(f"Outcome classes: {dict(outcomes)}")
    n = len(results)
    metrics = ["economy", "legitimacy", "military", "treasury", "leader_power"]
    for metric in metrics:
        vals = [r[metric] for r in results]
        mean = sum(vals) / n
        variance = sum((value - mean) ** 2 for value in vals) / n
        std = variance ** 0.5
        print(f"  {metric:14s}: mean={mean:.3f}  std={std:.3f}  min={min(vals):.3f}  max={max(vals):.3f}")


if __name__ == "__main__":
    results = run_batch(n_runs=20, n_steps=50, out_file="batch_results.csv")
    summarize(results)

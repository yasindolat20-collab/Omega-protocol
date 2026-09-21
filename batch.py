import random
import csv
from typing import Dict, List
from collections import Counter
from agent import Agent
from environment import Environment
from shared_memory import SharedMemory
from network import SocialNetwork
from leader import Leader

def run_once(seed: int, n_steps: int = 50) -> Dict:
    random.seed(seed)
    env = Environment()
    agents = [Agent(i) for i in range(100)]
    network = SocialNetwork(n_agents=100, k=4, p=0.1)
    for a in agents:
        a.set_neighbors(network.neighbors_of(a.id))
    leader = Leader(agent_id=0)
    shared = SharedMemory()
    for a in agents:
        a.set_shared_memory(shared)

    action_counter = Counter()
    detected_total = 0

    for step in range(1, n_steps + 1):
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
        for a in agents:
            a.learn(result)
        for a, act in zip(agents, actions):
            shared.add(a.id, act, result["outcome"].get(act, False), state)
        if step % 10 == 0:
            shared.decay_old()
        detected_total += leader.detect_gamers(agents, true_intents)
        for act in actions:
            action_counter[act] += 1

    fs = env.get_state()
    total = sum(action_counter.values()) if action_counter else 1

    # طبقه‌بندی نتیجه
    if fs["economy"] < 0.15 and fs["legitimacy"] < 0.30:
        outcome_class = "collapse"
    elif fs["legitimacy"] > 0.75 and fs["military"] > 0.35:
        outcome_class = "stable"
    elif fs["legitimacy"] > 0.5 and abs(fs["economy"] - 0.5) < 0.2:
        outcome_class = "equilibrium"
    else:
        outcome_class = "mixed"

    return {
        "seed": seed,
        "economy": round(fs["economy"], 4),
        "legitimacy": round(fs["legitimacy"], 4),
        "military": round(fs["military"], 4),
        "treasury": round(fs["treasury"], 4),
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
        r = run_once(seed, n_steps)
        results.append(r)
        print(f"Run {i+1:2d} | seed={seed} | {r['outcome_class']:11s} | econ={r['economy']:.2f} legit={r['legitimacy']:.2f} mil={r['military']:.2f}")
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved {len(results)} runs to {out_file}")
    return results

def summarize(results: List[Dict]):
    print("\n=== SUMMARY ===")
    outcomes = Counter(r["outcome_class"] for r in results)
    print(f"Outcome classes: {dict(outcomes)}")
    n = len(results)
    for key in ["economy", "legitimacy", "military", "treasury", "leader_power"]:
        vals = [r[key] for r in results]
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / n
        std = var ** 0.5
        print(f"  {key:14s}: mean={mean:.3f}  std={std:.3f}  min={min(vals):.3f}  max={max(vals):.3f}")

if __name__ == "__main__":
    results = run_batch(n_runs=20, n_steps=50)
    summarize(results)

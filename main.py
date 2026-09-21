import random
from collections import Counter
from rich.console import Console
from rich.table import Table
from agent import Agent, STRATEGIES
from environment import Environment
from shared_memory import SharedMemory
from logger import SimulationLogger
from network import SocialNetwork
from leader import Leader

console = Console()

def main():
    random.seed(42)
    env = Environment()
    agents = [Agent(i) for i in range(100)]

    network = SocialNetwork(n_agents=100, k=4, p=0.1)
    for agent in agents:
        agent.set_neighbors(network.neighbors_of(agent.id))

    leader = Leader(agent_id=0)
    shared = SharedMemory()
    for agent in agents:
        agent.set_shared_memory(shared)

    logger = SimulationLogger("simulation.csv")
    console.print("[bold cyan]Omega Protocol - Self-Awareness Edition[/bold cyan]\n")

    strategy_counts = Counter(a.strategy for a in agents)
    console.print(f"[cyan]Strategies: {dict(strategy_counts)}[/cyan]\n")

    total_detected = 0
    for step in range(1, 51):
        shock = env.shock()
        state = env.get_state()
        leader.update_power(state)
        command = leader.issue_command(state)

        actions = []
        neighbor_actions = {}
        true_intents = {}

        for agent in agents:
            agent.perceive(state)
            action = agent.decide(
                state,
                neighbor_actions=neighbor_actions if neighbor_actions else None,
                leader_command=command,
                leader_power=leader.power,
            )
            actions.append(action)
            neighbor_actions[agent.id] = action
            true_intents[agent.id] = agent._true_intent

        result = env.step(actions)

        for agent in agents:
            agent.learn(result)
        for agent, action in zip(agents, actions):
            success = result["outcome"].get(action, False)
            shared.add(agent.id, action, success, state)

        # رهبر رصد می‌کند
        detected = leader.detect_gamers(agents, true_intents)
        total_detected += detected

        if step % 10 == 0:
            shared.decay_old()

        logger.log(step, result["counts"], result["state"], shock)

        if step % 5 == 0 or step == 1:
            c = result["counts"]; s = result["state"]
            console.print(f"[bold]Step {step:2d}[/bold] | Cmd:[magenta]{command:9s}[/magenta] Pwr:{leader.power:.2f} Det:{detected:2d} | Loy:{c['Loyalty']:3d} Exit:{c['Exit']:3d} Voice:{c['Voice']:3d} Reb:{c['Rebellion']:3d}")

    logger.save()

    console.print("\n[bold green]=== Final Report ===[/bold green]")
    fc = Counter()
    for a in agents:
        for e in a.memory:
            fc[e["action"]] += 1
    t = Table(title="Action Distribution (Displayed)")
    t.add_column("Action", style="cyan"); t.add_column("Count", style="magenta")
    for act in ["Loyalty","Exit","Voice","Rebellion"]:
        t.add_row(act, str(fc.get(act, 0)))
    console.print(t)

    # توزیع استراتژی‌ها
    strat_t = Table(title="Strategy Distribution")
    strat_t.add_column("Strategy", style="cyan"); strat_t.add_column("Count", style="magenta")
    for s in STRATEGIES:
        strat_t.add_row(s, str(strategy_counts.get(s, 0)))
    console.print(strat_t)

    fs = env.get_state()
    console.print(f"\n[bold]Final - Econ:{fs['economy']:.3f} Legit:{fs['legitimacy']:.3f} Mil:{fs['military']:.3f} Treas:{fs['treasury']:.3f}[/bold]")
    console.print(f"[bold]Final Leader Power: {leader.power:.3f}[/bold]")
    console.print(f"[bold]Total Detected (Gamers/Hiders): {total_detected}[/bold]")
    console.print(f"[bold]Shared Memory: {len(shared.experiences)}[/bold]")

if __name__ == "__main__":
    main()

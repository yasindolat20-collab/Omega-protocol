import random
from collections import Counter
from rich.console import Console
from rich.table import Table
from agent import Agent
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

    # رهبر: ایجنت 0
    leader = Leader(agent_id=0)

    shared = SharedMemory()
    for agent in agents:
        agent.set_shared_memory(shared)

    logger = SimulationLogger("simulation.csv")
    console.print("[bold cyan]Omega Protocol - Leadership Edition[/bold cyan]\n")

    for step in range(1, 51):
        shock = env.shock()
        state = env.get_state()

        # رهبر فرمان می‌دهد و قدرتش را به‌روز می‌کند
        leader.update_power(state)
        command = leader.issue_command(state, {})

        actions = []
        neighbor_actions = {}
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

        result = env.step(actions)

        for agent in agents:
            agent.learn(result)
        for agent, action in zip(agents, actions):
            success = result["outcome"].get(action, False)
            shared.add(agent.id, action, success, state)

        if step % 10 == 0:
            shared.decay_old()

        logger.log(step, result["counts"], result["state"], shock)

        if step % 5 == 0 or step == 1:
            c = result["counts"]; s = result["state"]
            console.print(f"[bold]Step {step:2d}[/bold] | Cmd:[magenta]{command:9s}[/magenta] Pwr:{leader.power:.2f} | Loy:{c['Loyalty']:3d} Exit:{c['Exit']:3d} Voice:{c['Voice']:3d} Reb:{c['Rebellion']:3d} | Legit:{s['legitimacy']:.2f} Treas:{s['treasury']:.2f}")

    logger.save()

    console.print("\n[bold green]=== Final Report ===[/bold green]")
    fc = Counter()
    for a in agents:
        for e in a.memory:
            fc[e["action"]] += 1
    t = Table(title="Action Distribution")
    t.add_column("Action", style="cyan"); t.add_column("Count", style="magenta")
    for act in ["Loyalty","Exit","Voice","Rebellion"]:
        t.add_row(act, str(fc.get(act, 0)))
    console.print(t)

    fs = env.get_state()
    console.print(f"\n[bold]Final - Econ:{fs['economy']:.3f} Legit:{fs['legitimacy']:.3f} Mil:{fs['military']:.3f} Treas:{fs['treasury']:.3f}[/bold]")
    console.print(f"[bold]Final Leader Power: {leader.power:.3f}[/bold]")
    avg = sum(a.risk_aversion for a in agents) / len(agents)
    console.print(f"[bold]Avg Risk Aversion: {avg:.3f}[/bold]")

if __name__ == "__main__":
    main()

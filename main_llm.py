import random
from collections import Counter
from rich.console import Console
from rich.table import Table
from agent import Agent
from environment import Environment
from shared_memory import SharedMemory
from logger import SimulationLogger
from network import SocialNetwork
from leader_llm import LeaderLLM
from llm_gateway import LLMGateway
from llm_client import LLMClient

console = Console()


def main():
    random.seed(42)
    env = Environment()
    gateway = LLMGateway()
    llm = LLMClient(gateway)

    agents = []
    for i in range(100):
        use_llm = (i < 20)
        a = Agent(i, use_llm=use_llm)
        if use_llm:
            a.set_llm(llm)
        agents.append(a)

    network = SocialNetwork(n_agents=100, k=4, p=0.1)
    for a in agents:
        a.set_neighbors(network.neighbors_of(a.id))

    leader = LeaderLLM(agent_id=0, gateway=gateway)
    shared = SharedMemory()
    for a in agents:
        a.set_shared_memory(shared)

    logger = SimulationLogger("simulation_llm.csv")
    console.print("[bold cyan]Omega Protocol - LLM Edition (Leader + 20 Agents)[/bold cyan]\n")

    for step in range(1, 21):
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

        detected = leader.detect_gamers(agents, true_intents)
        logger.log(step, result["counts"], result["state"], None)

        c = result["counts"]; s = result["state"]
        console.print(f"[bold]Step {step:2d}[/bold] | Cmd:[magenta]{command:9s}[/magenta] Det:{detected:2d} | Loy:{c['Loyalty']:3d} Exit:{c['Exit']:3d} Voice:{c['Voice']:3d} Reb:{c['Rebellion']:3d}")

    logger.save()

    console.print("\n[bold green]=== Final Report ===[/bold green]")
    fc = Counter()
    for a in agents:
        for e in a.memory:
            fc[e["action"]] += 1
    t = Table(title="Action Distribution")
    t.add_column("Action", style="cyan"); t.add_column("Count", style="magenta")
    for act in ["Loyalty", "Exit", "Voice", "Rebellion"]:
        t.add_row(act, str(fc.get(act, 0)))
    console.print(t)

    console.print("\n[bold green]=== LLM Stats ===[/bold green]")
    console.print(f"Gateway: {gateway.get_stats()}")
    console.print(f"Client: calls={llm.calls}, cache_hits={llm.cache_hits}")

    fs = env.get_state()
    console.print(f"\n[bold]Final - Econ:{fs['economy']:.3f} Legit:{fs['legitimacy']:.3f} Mil:{fs['military']:.3f} Treas:{fs['treasury']:.3f}[/bold]")


if __name__ == "__main__":
    main()

"""
مقایسه LLM vs قاعده‌محور
"""
import random
import csv
from collections import Counter
from rich.console import Console
from rich.table import Table

console = Console()


def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def summarize(path, label):
    rows = load_csv(path)
    if not rows:
        return None
    total = Counter()
    for r in rows:
        for k in ["loyalty", "exit", "voice", "rebellion"]:
            total[k] += int(r[k])
    grand = sum(total.values()) or 1
    fs = rows[-1]
    return {
        "label": label,
        "loyalty_pct": round(100 * total["loyalty"] / grand, 1),
        "exit_pct": round(100 * total["exit"] / grand, 1),
        "voice_pct": round(100 * total["voice"] / grand, 1),
        "rebellion_pct": round(100 * total["rebellion"] / grand, 1),
        "final_econ": float(fs["economy"]),
        "final_legit": float(fs["legitimacy"]),
        "final_mil": float(fs["military"]),
        "final_treas": float(fs["treasury"]),
    }


if __name__ == "__main__":
    results = []
    for path, label in [("simulation.csv", "Rule-based"), ("simulation_llm.csv", "LLM")]:
        r = summarize(path, label)
        if r:
            results.append(r)

    t = Table(title="LLM vs Rule-based Comparison")
    t.add_column("Metric", style="cyan")
    for r in results:
        t.add_column(r["label"], style="magenta")

    for metric in ["loyalty_pct", "exit_pct", "voice_pct", "rebellion_pct",
                   "final_econ", "final_legit", "final_mil", "final_treas"]:
        row = [metric]
        for r in results:
            row.append(str(r.get(metric, "—")))
        t.add_row(*row)

    console.print(t)

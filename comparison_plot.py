import csv
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


METRICS = ["loyalty", "exit", "voice", "rebellion"]


def load_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(rows):
    if not rows:
        return {"loyalty_pct": 0.0, "exit_pct": 0.0, "voice_pct": 0.0, "rebellion_pct": 0.0,
            "final_economy": 0.0, "final_legitimacy": 0.0}
    counts = Counter({key: 0 for key in METRICS})
    total = 0
    for row in rows:
        for key in METRICS:
            counts[key] += int(row.get(key, 0))
            total += int(row.get(key, 0))
    last = rows[-1]
    return {
        "loyalty_pct": round(100 * counts["loyalty"] / total, 2) if total else 0.0,
        "exit_pct": round(100 * counts["exit"] / total, 2) if total else 0.0,
        "voice_pct": round(100 * counts["voice"] / total, 2) if total else 0.0,
        "rebellion_pct": round(100 * counts["rebellion"] / total, 2) if total else 0.0,
        "final_economy": float(last.get("economy", 0.0)),
        "final_legitimacy": float(last.get("legitimacy", 0.0)),
    }


def build_comparison():
    series = {}
    for file_name, label in [("simulation.csv", "Rule-based"), ("simulation_llm.csv", "LLM")]:
        rows = load_csv(file_name) if __import__("os").path.exists(file_name) else []
        series[label] = summarize(rows)

    labels = ["Loyalty %", "Exit %", "Voice %", "Rebellion %", "Final Economy", "Final Legitimacy"]
    values = {
        "Rule-based": [
            series["Rule-based"]["loyalty_pct"],
            series["Rule-based"]["exit_pct"],
            series["Rule-based"]["voice_pct"],
            series["Rule-based"]["rebellion_pct"],
            series["Rule-based"]["final_economy"],
            series["Rule-based"]["final_legitimacy"],
        ],
        "LLM": [
            series["LLM"]["loyalty_pct"],
            series["LLM"]["exit_pct"],
            series["LLM"]["voice_pct"],
            series["LLM"]["rebellion_pct"],
            series["LLM"]["final_economy"],
            series["LLM"]["final_legitimacy"],
        ],
    }

    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharey=False)
    axes = axes.flatten()
    for idx, label in enumerate(labels):
        ax = axes[idx]
        bar_values = [values["Rule-based"][idx], values["LLM"][idx]]
        bars = ax.bar(["Rule-based", "LLM"], bar_values, color=["steelblue", "darkorange"])
        ax.set_title(label)
        ax.grid(axis="y", alpha=0.3)
        for bar, value in zip(bars, bar_values):
            height = value
            ax.text(bar.get_x() + bar.get_width() / 2, height + max(0.01, abs(height) * 0.05), f"{value:.2f}", ha="center", va="bottom", fontsize=8)

    for ax in axes[len(labels):]:
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("comparison_plot.png", dpi=120)
    print("Saved comparison_plot.png")


if __name__ == "__main__":
    build_comparison()

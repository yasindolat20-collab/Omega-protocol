import csv
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load(filename="batch_results.csv"):
    with open(filename, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def plot_batch(filename="batch_results.csv"):
    rows = load(filename)
    outcomes = [r["outcome_class"] for r in rows]
    econ = [float(r["economy"]) for r in rows]
    legit = [float(r["legitimacy"]) for r in rows]
    mil = [float(r["military"]) for r in rows]
    loy = [float(r["loyalty_pct"]) for r in rows]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Outcome classes
    ax = axes[0, 0]
    counts = Counter(outcomes)
    colors_map = {"collapse": "red", "stable": "green", "equilibrium": "blue", "mixed": "orange"}
    bars = ax.bar(counts.keys(), counts.values(),
                  color=[colors_map.get(k, "gray") for k in counts.keys()])
    ax.set_title("Outcome Distribution (20 runs)")
    ax.set_ylabel("Count")
    for b, v in zip(bars, counts.values()):
        ax.text(b.get_x() + b.get_width()/2, v + 0.1, str(v), ha="center")

    # Scatter: economy vs legitimacy
    ax = axes[0, 1]
    for oc in set(outcomes):
        xs = [econ[i] for i in range(len(rows)) if outcomes[i] == oc]
        ys = [legit[i] for i in range(len(rows)) if outcomes[i] == oc]
        ax.scatter(xs, ys, label=oc, s=80, alpha=0.7, color=colors_map.get(oc, "gray"))
    ax.set_xlabel("Economy"); ax.set_ylabel("Legitimacy")
    ax.set_title("Phase Space: Economy vs Legitimacy")
    ax.legend(); ax.grid(True, alpha=0.3)

    # Distribution of final economy
    ax = axes[1, 0]
    ax.hist(econ, bins=10, color="green", alpha=0.7, edgecolor="black")
    ax.set_title("Distribution of Final Economy")
    ax.set_xlabel("Economy"); ax.set_ylabel("Count")
    ax.grid(True, alpha=0.3)

    # Distribution of loyalty %
    ax = axes[1, 1]
    ax.hist(loy, bins=10, color="blue", alpha=0.7, edgecolor="black")
    ax.set_title("Distribution of Loyalty % (across runs)")
    ax.set_xlabel("Loyalty %"); ax.set_ylabel("Count")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("batch_plot.png", dpi=100)
    print("Saved batch_plot.png")

if __name__ == "__main__":
    plot_batch()

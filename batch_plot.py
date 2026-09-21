import csv
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load(filename="batch_results.csv"):
    with open(filename, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def plot_batch(filename="batch_results.csv"):
    rows = load(filename)
    if not rows:
        raise ValueError(f"No rows available in {filename!r}.")

    outcomes = [row["outcome_class"] for row in rows]
    economy = [float(row["economy"]) for row in rows]
    legitimacy = [float(row["legitimacy"]) for row in rows]
    loyalty = [float(row["loyalty_pct"]) for row in rows]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax = axes[0, 0]
    counts = Counter(outcomes)
    colors_map = {"collapse": "red", "stable": "green", "equilibrium": "blue", "mixed": "orange"}
    order = ["collapse", "stable", "equilibrium", "mixed"]
    values = [counts.get(label, 0) for label in order]
    bar_labels = [label for label in order if counts.get(label, 0) > 0 or label in counts]
    bar_values = [counts.get(label, 0) for label in bar_labels]
    colors = [colors_map.get(label, "gray") for label in bar_labels]
    bars = ax.bar(bar_labels, bar_values, color=colors)
    ax.set_title("Outcome Distribution")
    ax.set_xlabel("Outcome Class")
    ax.set_ylabel("Count")
    ax.grid(axis="y", alpha=0.3)
    for bar, value in zip(bars, bar_values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.05, str(value), ha="center", va="bottom")

    ax = axes[0, 1]
    for outcome_class in sorted(set(outcomes)):
        xs = [economy[i] for i, outcome in enumerate(outcomes) if outcome == outcome_class]
        ys = [legitimacy[i] for i, outcome in enumerate(outcomes) if outcome == outcome_class]
        ax.scatter(xs, ys, label=outcome_class, s=80, alpha=0.8, color=colors_map.get(outcome_class, "gray"))
    ax.set_title("Economy vs Legitimacy")
    ax.set_xlabel("Economy")
    ax.set_ylabel("Legitimacy")
    ax.grid(True, alpha=0.3)
    ax.legend()

    ax = axes[1, 0]
    ax.hist(economy, bins=10, color="green", alpha=0.7, edgecolor="black")
    ax.set_title("Economy Histogram")
    ax.set_xlabel("Economy")
    ax.set_ylabel("Count")
    ax.grid(True, alpha=0.3)

    ax = axes[1, 1]
    ax.hist(loyalty, bins=10, color="skyblue", alpha=0.7, edgecolor="black")
    ax.set_title("Loyalty Histogram")
    ax.set_xlabel("Loyalty %")
    ax.set_ylabel("Count")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = "batch_plot.png"
    plt.savefig(out_path, dpi=120)
    print(f"Saved {out_path}")
    return out_path


if __name__ == "__main__":
    plot_batch()

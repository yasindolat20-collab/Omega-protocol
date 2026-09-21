import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_data(filename):
    with open(filename, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def choose_file(primary="simulation_llm.csv", fallback="simulation.csv"):
    if os.path.exists(primary):
        return primary
    if os.path.exists(fallback):
        return fallback
    raise FileNotFoundError(f"No simulation data found at {primary!r} or {fallback!r}.")


def plot_all(filename=None):
    if filename is None:
        filename = choose_file()
    rows = load_data(filename)
    if not rows:
        raise ValueError(f"No rows in {filename!r}.")
    steps = [int(r.get("step", i + 1)) for i, r in enumerate(rows)]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax = axes[0, 0]
    ax.plot(steps, [int(r.get("loyalty", 0)) for r in rows], label="Loyalty", color="blue")
    ax.plot(steps, [int(r.get("exit", 0)) for r in rows], label="Exit", color="orange")
    ax.plot(steps, [int(r.get("voice", 0)) for r in rows], label="Voice", color="green")
    ax.plot(steps, [int(r.get("rebellion", 0)) for r in rows], label="Rebellion", color="red")
    ax.set_title("Action Distribution")
    ax.set_xlabel("Step")
    ax.set_ylabel("Count")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[0, 1]
    ax.plot(steps, [float(r.get("economy", 0.0)) for r in rows], label="Economy", color="darkgreen")
    ax.plot(steps, [float(r.get("legitimacy", 0.0)) for r in rows], label="Legitimacy", color="purple")
    ax.plot(steps, [float(r.get("military", 0.0)) for r in rows], label="Military", color="brown")
    ax.plot(steps, [float(r.get("treasury", 0.0)) for r in rows], label="Treasury", color="gold")
    ax.set_title("Environment Variables")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[1, 0]
    loy = [int(r.get("loyalty", 0)) for r in rows]
    ext = [int(r.get("exit", 0)) for r in rows]
    voi = [int(r.get("voice", 0)) for r in rows]
    reb = [int(r.get("rebellion", 0)) for r in rows]
    ax.stackplot(steps, loy, ext, voi, reb,
                 labels=["Loyalty", "Exit", "Voice", "Rebellion"],
                 colors=["blue", "orange", "green", "red"], alpha=0.7)
    ax.set_title("Stacked Actions")
    ax.set_xlabel("Step")
    ax.set_ylabel("Count")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    ax = axes[1, 1]
    shock_present = "shock" in rows[0].keys() if rows[0] else False
    if shock_present:
        shock_steps = [int(r["step"]) for r in rows if r.get("shock")]
        shock_types = [r.get("shock") for r in rows if r.get("shock")]
        color_map = {"war": "red", "famine": "orange", "crisis": "purple"}
        for s, t in zip(shock_steps, shock_types):
            ax.axvline(x=s, color=color_map.get(t, "gray"), alpha=0.6, linestyle="--")
    ax.plot(steps, [float(r.get("legitimacy", 0.0)) for r in rows], color="purple", label="Legitimacy")
    ax.plot(steps, [float(r.get("economy", 0.0)) for r in rows], color="green", label="Economy")
    ax.set_title("Shocks vs Environment")
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = "simulation_plot.png"
    plt.savefig(out_path, dpi=100)
    print(f"Saved {out_path}")
    return out_path


if __name__ == "__main__":
    plot_all()

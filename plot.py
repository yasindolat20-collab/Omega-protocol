import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load_data(filename="simulation.csv"):
    rows = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def plot_all(filename="simulation.csv"):
    rows = load_data(filename)
    steps = [int(r["step"]) for r in rows]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # نمودار ۱: توزیع اعمال
    ax = axes[0, 0]
    ax.plot(steps, [int(r["loyalty"]) for r in rows], label="Loyalty", color="blue")
    ax.plot(steps, [int(r["exit"]) for r in rows], label="Exit", color="orange")
    ax.plot(steps, [int(r["voice"]) for r in rows], label="Voice", color="green")
    ax.plot(steps, [int(r["rebellion"]) for r in rows], label="Rebellion", color="red")
    ax.set_title("Action Distribution over Time")
    ax.set_xlabel("Step"); ax.set_ylabel("Count")
    ax.legend(); ax.grid(True, alpha=0.3)

    # نمودار ۲: متغیرهای محیط
    ax = axes[0, 1]
    ax.plot(steps, [float(r["economy"]) for r in rows], label="Economy", color="darkgreen")
    ax.plot(steps, [float(r["legitimacy"]) for r in rows], label="Legitimacy", color="purple")
    ax.plot(steps, [float(r["military"]) for r in rows], label="Military", color="brown")
    ax.plot(steps, [float(r["treasury"]) for r in rows], label="Treasury", color="gold")
    ax.set_title("Environment Variables")
    ax.set_xlabel("Step"); ax.set_ylabel("Value")
    ax.legend(); ax.grid(True, alpha=0.3)

    # نمودار ۳: سهم اعمال (Stacked)
    ax = axes[1, 0]
    loy = [int(r["loyalty"]) for r in rows]
    ext = [int(r["exit"]) for r in rows]
    voi = [int(r["voice"]) for r in rows]
    reb = [int(r["rebellion"]) for r in rows]
    ax.stackplot(steps, loy, ext, voi, reb,
                 labels=["Loyalty", "Exit", "Voice", "Rebellion"],
                 colors=["blue", "orange", "green", "red"], alpha=0.7)
    ax.set_title("Stacked Action Share")
    ax.set_xlabel("Step"); ax.set_ylabel("Count")
    ax.legend(loc="upper right"); ax.grid(True, alpha=0.3)

    # نمودار ۴: شوک‌ها
    ax = axes[1, 1]
    shock_steps = [int(r["step"]) for r in rows if r["shock"]]
    shock_types = [r["shock"] for r in rows if r["shock"]]
    colors = {"war": "red", "famine": "orange", "crisis": "purple"}
    for s, t in zip(shock_steps, shock_types):
        ax.axvline(x=s, color=colors.get(t, "gray"), alpha=0.5, linestyle="--")
    ax.plot(steps, [float(r["legitimacy"]) for r in rows], color="purple", label="Legitimacy")
    ax.plot(steps, [float(r["economy"]) for r in rows], color="green", label="Economy")
    ax.set_title("Shocks vs Environment")
    ax.set_xlabel("Step"); ax.set_ylabel("Value")
    ax.legend(); ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("simulation_plot.png", dpi=100)
    print("Saved plot to simulation_plot.png")
    return True

if __name__ == "__main__":
    plot_all()

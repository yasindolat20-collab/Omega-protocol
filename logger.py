import csv
from typing import Dict

class SimulationLogger:
    def __init__(self, filename="simulation.csv"):
        self.filename = filename
        self.rows = []

    def log(self, step, counts, state, shock=None):
        self.rows.append({
            "step": step,
            "loyalty": counts["Loyalty"],
            "exit": counts["Exit"],
            "voice": counts["Voice"],
            "rebellion": counts["Rebellion"],
            "economy": round(state["economy"], 4),
            "legitimacy": round(state["legitimacy"], 4),
            "military": round(state["military"], 4),
            "treasury": round(state["treasury"], 4),
            "shock": shock if shock else "",
        })

    def save(self):
        if not self.rows:
            return
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            writer.writeheader()
            writer.writerows(self.rows)
        print(f"Saved {len(self.rows)} rows to {self.filename}")

import csv
import random

patients = [
    {"name": "Ramesh Kumar", "age": 72, "risk": "high"},
    {"name": "Sunita Mehta", "age": 68, "risk": "medium"},
    {"name": "Anita Verma", "age": 65, "risk": "medium"},
    {"name": "Priya Gupta", "age": 59, "risk": "low"},
]

rows = []
for p in patients:
    for day in range(7):
        if p["risk"] == "high":
            sleep = round(random.uniform(2.5, 4.0), 1)
            steps = random.randint(800, 2000)
            wandering = random.randint(2, 5)
        elif p["risk"] == "medium":
            sleep = round(random.uniform(4.5, 6.0), 1)
            steps = random.randint(2000, 4000)
            wandering = random.randint(0, 2)
        else:
            sleep = round(random.uniform(6.5, 8.0), 1)
            steps = random.randint(5000, 8000)
            wandering = 0

        rows.append({
            "patient": p["name"],
            "age": p["age"],
            "day": day + 1,
            "sleep_hrs": sleep,
            "steps": steps,
            "wandering_events": wandering,
        })

with open("data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Data ready! data.csv ban gayi!")

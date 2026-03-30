import csv
import random

def calculate_score(sleep, steps, wandering):
    score = 100
    
    if sleep < 4:
        score -= 40
    elif sleep < 6:
        score -= 20
    
    if steps < 2000:
        score -= 30
    elif steps < 4000:
        score -= 15
    
    if wandering >= 3:
        score -= 30
    elif wandering >= 1:
        score -= 10
    
    return max(0, score)

def get_risk(score):
    if score < 40:
        return "HIGH RISK"
    elif score < 65:
        return "MEDIUM"
    else:
        return "NORMAL"

with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    patients = {}
    for row in reader:
        name = row["patient"]
        if name not in patients:
            patients[name] = []
        patients[name].append(row)

print("\n=== CogniWatch AI Analysis ===\n")
for name, records in patients.items():
    avg_sleep = sum(float(r["sleep_hrs"]) for r in records) / len(records)
    avg_steps = sum(int(r["steps"]) for r in records) / len(records)
    avg_wander = sum(int(r["wandering_events"]) for r in records) / len(records)
    
    score = calculate_score(avg_sleep, avg_steps, avg_wander)
    risk = get_risk(score)
    
    print(f"Patient: {name}")
    print(f"  Avg Sleep:     {avg_sleep:.1f} hrs")
    print(f"  Avg Steps:     {int(avg_steps)}")
    print(f"  Wandering:     {avg_wander:.1f} events/day")
    print(f"  Cognitive Score: {score}/100")
    print(f"  Risk Level:    {risk}")
    print()

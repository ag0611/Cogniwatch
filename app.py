from flask import Flask, jsonify
from flask_cors import CORS
import csv
import random
import threading
import time

app = Flask(__name__)
CORS(app)

def update_data():
    while True:
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
        time.sleep(5)

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

@app.route('/patients')
def get_patients():
    patients = {}
    with open("data.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["patient"]
            if name not in patients:
                patients[name] = []
            patients[name].append(row)

    result = []
    for name, records in patients.items():
        avg_sleep = sum(float(r["sleep_hrs"]) for r in records) / len(records)
        avg_steps = sum(int(r["steps"]) for r in records) / len(records)
        avg_wander = sum(int(r["wandering_events"]) for r in records) / len(records)
        score = calculate_score(avg_sleep, avg_steps, avg_wander)
        result.append({
            "name": name,
            "age": records[0]["age"],
            "sleep": round(avg_sleep, 1),
            "steps": int(avg_steps),
            "wandering": round(avg_wander, 1),
            "score": score,
            "risk": get_risk(score)
        })
    return jsonify(result)

thread = threading.Thread(target=update_data)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    app.run(debug=True)
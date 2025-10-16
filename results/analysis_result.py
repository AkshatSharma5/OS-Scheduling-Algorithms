import matplotlib.pyplot as plt
from statistics import mean

# Import scheduling algorithms
import _1_fcfs as fcfs
import _2_sjf_nonpreemptive as sjf_np
import _3_sjf_preemptive as sjf_p
import _4_round_robin as rr
import _5_priority_nonpreemptive as pri_np


# ---------------------- Common Task Definition ----------------------

class Task:
    def __init__(self, name, burst, arrival, priority=0):
        self.name = name
        self.burst = burst
        self.arrival = arrival
        self.priority = priority


# ---------------------- Helper Function ----------------------

def compute_metrics(results):
    """Given a list of (task_name, start, end) tuples, compute metrics."""
    task_data = {}
    for name, start, end in results:
        if name not in task_data:
            task_data[name] = {"start": [], "end": [], "total": 0}
        task_data[name]["start"].append(start)
        task_data[name]["end"].append(end)

    metrics = {}
    for name, data in task_data.items():
        burst = sum(e - s for s, e in zip(data["start"], data["end"]))
        completion = data["end"][-1]
        arrival = next(t.arrival for t in TASKS if t.name == name)
        tat = completion - arrival
        wt = tat - burst
        metrics[name] = {"TAT": tat, "WT": wt, "CT": completion}

    avg_tat = mean(v["TAT"] for v in metrics.values())
    avg_wt = mean(v["WT"] for v in metrics.values())
    return avg_tat, avg_wt, metrics


# ---------------------- Task Set ----------------------

TASKS = [
    Task("T1", 6, 0, 2),
    Task("T2", 8, 1, 1),
    Task("T3", 7, 2, 3),
    Task("T4", 3, 3, 2)
]


# ---------------------- Run Each Scheduler ----------------------

QUANTUM = 3
results = {}

results["FCFS"] = fcfs.run_scheduler(TASKS)
results["SJF Non-Preemptive"] = sjf_np.run_scheduler(TASKS)
results["SJF Preemptive"] = sjf_p.run_scheduler(TASKS)
results["Round Robin"] = rr.run_scheduler(TASKS, QUANTUM)
results["Priority Non-Preemptive"] = pri_np.run_scheduler(TASKS)

# ---------------------- Compute Metrics ----------------------

analysis = {}
for algo, res in results.items():
    avg_tat, avg_wt, _ = compute_metrics(res)
    analysis[algo] = {"Avg_TAT": avg_tat, "Avg_WT": avg_wt}

# ---------------------- Display Table ----------------------

print("\n================= COMPARATIVE ANALYSIS =================\n")
print(f"{'Algorithm':30} {'Avg TAT':>10} {'Avg WT':>10}")
print("-" * 55)
for algo, data in analysis.items():
    print(f"{algo:30} {data['Avg_TAT']:10.2f} {data['Avg_WT']:10.2f}")

# ---------------------- Plot Graph ----------------------

algos = list(analysis.keys())
avg_tats = [analysis[a]["Avg_TAT"] for a in algos]
avg_wts = [analysis[a]["Avg_WT"] for a in algos]

plt.figure(figsize=(8,4))
plt.barh(algos, avg_tats, label="Avg Turnaround Time")
plt.barh(algos, avg_wts, left=avg_tats, label="Avg Waiting Time")
plt.xlabel("Time (ms)")
plt.title("Scheduler Performance Comparison")
plt.legend()
plt.tight_layout()
plt.show()

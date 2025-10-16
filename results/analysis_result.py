# -------------------- Comparative Analysis of All Scheduling Algorithms --------------------
# This script imports all algorithms from /algorithms and compares:
# - Average Waiting Time
# - Average Turnaround Time
# - Optionally checks deadline misses
#
# It uses the shared Task dataclass and helper utilities from utils.py.

from utils import Task, finalize_tasks
from algorithms.fcfs import fcfs_scheduler
from algorithms.sjf_non_preemptive import sjf_nonpreemptive
from algorithms.sjf_preemptive import sjf_preemptive
from algorithms.preemptive_priority import priority_preemptive
from algorithms.round_robin import round_robin
import matplotlib.pyplot as plt


def average_metrics(task_list):
    """Compute average waiting and turnaround times."""
    avg_wait = sum(t.waiting for t in task_list if t.waiting is not None) / len(task_list)
    avg_tat = sum(t.turnaround for t in task_list if t.turnaround is not None) / len(task_list)
    return avg_wait, avg_tat


def compare_algorithms():
    """Run all schedulers on the same base tasks and display comparative results."""
    # (name, burst, arrival, priority)
    base_tasks = [
        ("T1", 5, 0, 2),
        ("T2", 8, 1, 1),
        ("T3", 6, 2, 3),
        ("T4", 4, 3, 2)
    ]

    # Create deep copies for each algorithm
    fcfs_tasks = [Task(n, b, a, p) for n, b, a, p in base_tasks]
    sjfN_tasks = [Task(n, b, a, p) for n, b, a, p in base_tasks]
    sjfP_tasks = [Task(n, b, a, p) for n, b, a, p in base_tasks]
    pri_tasks  = [Task(n, b, a, p) for n, b, a, p in base_tasks]
    rr_tasks   = [Task(n, b, a, p) for n, b, a, p in base_tasks]

    # Execute each scheduler
    _, fcfs_done = fcfs_scheduler(fcfs_tasks)
    _, sjfN_done = sjf_nonpreemptive(sjfN_tasks)
    _, sjfP_done = sjf_preemptive(sjfP_tasks)
    _, pri_done  = priority_preemptive(pri_tasks)
    _, rr_done   = round_robin(rr_tasks, quantum=3)

    # Finalize metrics
    for group in [fcfs_done, sjfN_done, sjfP_done, pri_done, rr_done]:
        finalize_tasks(group)

    # Collect results
    results = {
        "FCFS": average_metrics(fcfs_done),
        "SJF (Non-preemptive)": average_metrics(sjfN_done),
        "SJF (Preemptive)": average_metrics(sjfP_done),
        "Priority (Preemptive)": average_metrics(pri_done),
        "Round Robin": average_metrics(rr_done)
    }

    # Print table
    print("\n--- Comparative Analysis ---")
    print(f"{'Algorithm':<25} {'Avg Waiting Time':<20} {'Avg Turnaround Time':<20}")
    for name, (w, t) in results.items():
        print(f"{name:<25} {w:<20.2f} {t:<20.2f}")

    # Visual comparison
    algos = list(results.keys())
    wait_times = [v[0] for v in results.values()]
    tat_times = [v[1] for v in results.values()]

    plt.figure(figsize=(9, 5))
    plt.bar(algos, wait_times, label="Avg Waiting Time")
    plt.bar(algos, tat_times, bottom=wait_times, label="Avg Turnaround Time")
    plt.ylabel("Time Units")
    plt.title("Scheduler Performance Comparison")
    plt.xticks(rotation=20)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    compare_algorithms()

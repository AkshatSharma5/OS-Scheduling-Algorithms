# First-Come First-Served Scheduler (non-preemptive)
# Reads a list of Task objects and simulates FCFS scheduling.
# Produces gantt_log (list of (start_time, task_name)) and updates task completion times.

from typing import List, Tuple
from utils import Task, finalize_tasks

def fcfs_scheduler(tasks: List[Task]) -> Tuple[List[Tuple[int, str]], float]:
    """
    FCFS: schedule tasks in order of arrival time (tie-breaker: name).
    Returns: (gantt_log, cpu_utilization_percentage)
    The gantt_log is a list of tuples: (start_time, task_name).
    Each scheduler should update task.start_times, task.end_times and task.completion.
    """
    # Caller should pass fresh tasks or recreate between runs.
    tasks.sort(key=lambda t: (t.arrival, t.name))

    time = 0
    gantt = []
    idle_time = 0

    for t in tasks:
        # Advance time if CPU idle until the task arrives
        if time < t.arrival:
            # CPU idle interval from time -> t.arrival
            # We'll represent idle by appending an "IDLE" segment start
            gantt.append((time, "IDLE"))
            idle_time += (t.arrival - time)
            time = t.arrival

        # Start executing task t now
        t.start_times.append(time)
        gantt.append((time, t.name))
        time += t.burst
        t.end_times.append(time)
        t.remaining = 0
        t.completion = time

    total_time = time
    cpu_util = ((total_time - idle_time) / total_time) * 100 if total_time > 0 else 0.0

    finalize_tasks(tasks)
    return gantt, cpu_util

# Shortest Job First (non-preemptive)
# Among tasks that have arrived and are ready, pick the one with the smallest burst time.
# Non-preemptive: once chosen, run to completion.

from typing import List, Tuple
from utils import Task, finalize_tasks

def sjf_nonpreemptive(tasks: List[Task]) -> Tuple[List[Tuple[int, str]], float]:
    # We'll operate on the tasks list directly; caller should use fresh copies for each scheduler.
    tasks_sorted = sorted(tasks, key=lambda t: (t.arrival, t.burst, t.name))
    time = 0
    gantt = []
    idle_time = 0

    ready = []
    remaining_tasks = tasks_sorted.copy()

    while remaining_tasks or ready:
        # Fill ready queue with newly arrived tasks
        while remaining_tasks and remaining_tasks[0].arrival <= time:
            ready.append(remaining_tasks.pop(0))

        if not ready:
            # CPU idle: jump to next arrival (more efficient than stepping one unit)
            if remaining_tasks:
                upcoming = remaining_tasks[0].arrival
                gantt.append((time, "IDLE"))
                idle_time += (upcoming - time)
                time = upcoming
            continue

        # pick shortest burst among ready tasks
        ready.sort(key=lambda t: (t.burst, t.arrival, t.name))
        task = ready.pop(0)

        # run to completion
        task.start_times.append(time)
        gantt.append((time, task.name))
        time += task.burst
        task.end_times.append(time)
        task.remaining = 0
        task.completion = time

        # newly arrived tasks while this task ran will be appended at top of loop

    total_time = time
    cpu_util = ((total_time - idle_time) / total_time) * 100 if total_time > 0 else 0.0
    finalize_tasks(tasks)
    return gantt, cpu_util

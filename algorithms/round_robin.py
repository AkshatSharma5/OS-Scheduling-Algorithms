# -------------------- Round Robin Scheduling --------------------
# Each task gets a fixed quantum of CPU time.
# After its quantum expires, the next task is picked from the queue.

import matplotlib.pyplot as plt

class Task:
    def __init__(self, name, burst, arrival):
        self.name = name
        self.burst = burst
        self.remaining = burst
        self.arrival = arrival
        self.completion = 0
        self.start_times = []
        self.end_times = []

def round_robin(tasks, quantum):
    time = 0
    gantt = []
    ready_queue = [t for t in tasks if t.arrival <= time]

    while any(t.remaining > 0 for t in tasks):
        if not ready_queue:
            time += 1
            ready_queue = [t for t in tasks if t.arrival <= time and t.remaining > 0]
            continue

        task = ready_queue.pop(0)
        exec_time = min(task.remaining, quantum)

        task.start_times.append(time)
        gantt.append((time, task.name))
        time += exec_time
        task.remaining -= exec_time
        task.end_times.append(time)

        for t in tasks:
            if t.arrival <= time and t.remaining > 0 and t not in ready_queue and t != task:
                ready_queue.append(t)

        if task.remaining > 0:
            ready_queue.append(task)
        else:
            task.completion = time

    for t in tasks:
        t.turnaround = t.completion - t.arrival
        t.waiting = t.turnaround - t.burst

    return gantt, tasks

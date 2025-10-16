# -------------------- Priority Preemptive Scheduling --------------------
# CPU always executes the task with the highest priority (lowest number = higher priority)

class Task:
    def __init__(self, name, burst, arrival, priority):
        self.name = name
        self.burst = burst
        self.remaining = burst
        self.arrival = arrival
        self.priority = priority
        self.start = None
        self.completion = 0

def priority_preemptive(tasks):
    time = 0
    gantt = []
    remaining = [t for t in tasks]

    while any(t.remaining > 0 for t in remaining):
        available = [t for t in remaining if t.arrival <= time and t.remaining > 0]
        if not available:
            time += 1
            continue

        highest = min(available, key=lambda t: t.priority)
        if highest.start is None:
            highest.start = time

        gantt.append((time, highest.name))
        highest.remaining -= 1
        time += 1

        if highest.remaining == 0:
            highest.completion = time

    for t in remaining:
        t.turnaround = t.completion - t.arrival
        t.waiting = t.turnaround - t.burst

    return gantt, remaining

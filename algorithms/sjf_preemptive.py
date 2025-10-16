# Shortest Remaining Time First (preemptive SJF)
# At every time unit (or event), pick the ready task with the smallest remaining time.
# If a new task arrives with smaller remaining time, preempt the running task.

from typing import List, Tuple
from utils import Task, finalize_tasks

def srtf_scheduler(tasks: List[Task]) -> Tuple[List[Tuple[int, str]], float]:
    """
    Preemptive SJF (SRTF).
    We'll simulate in time steps but optimize by jumping to next event when possible.
    The gantt log format is (start_time, task_name).
    """
    # Initialize
    tasks_by_arrival = sorted(tasks, key=lambda t: (t.arrival, t.name))
    time = 0
    gantt = []
    idle_time = 0
    ready = []

    # index for tasks_by_arrival
    idx = 0
    current_task = None

    # Continue while tasks remain unfinished
    while idx < len(tasks_by_arrival) or ready or current_task:
        # Insert newly arrived tasks into ready list
        while idx < len(tasks_by_arrival) and tasks_by_arrival[idx].arrival <= time:
            ready.append(tasks_by_arrival[idx])
            idx += 1

        # pick the task with smallest remaining among ready + current
        candidates = ready.copy()
        if current_task and current_task.remaining > 0:
            candidates.append(current_task)

        if not candidates:
            # CPU idle: jump to next arrival time
            if idx < len(tasks_by_arrival):
                next_arrival = tasks_by_arrival[idx].arrival
                gantt.append((time, "IDLE"))
                idle_time += (next_arrival - time)
                time = next_arrival
                continue
            else:
                break

        # choose shortest remaining
        candidates.sort(key=lambda t: (t.remaining, t.arrival, t.name))
        chosen = candidates[0]

        # If chosen is not current, we are context switching to chosen
        if chosen is not current_task:
            # close current_task's last end_time if any
            current_task = chosen
            # If the chosen task was in ready list, remove it
            if chosen in ready:
                ready.remove(chosen)
            # record start time in gantt and task's start_times
            current_task.start_times.append(time)
            gantt.append((time, current_task.name))

        # Determine how long we can run: until next arrival that could preempt OR until completion
        if idx < len(tasks_by_arrival):
            next_arrival_time = tasks_by_arrival[idx].arrival
        else:
            next_arrival_time = None

        # If there is a next arrival and its arrival time comes before current finishes,
        # we only run until that arrival
        time_to_finish = current_task.remaining
        if next_arrival_time is not None:
            available_time = next_arrival_time - time
            # we run for min(available_time, time_to_finish)
            run_time = min(available_time if available_time > 0 else 0, time_to_finish)
            if run_time == 0:
                # immediate arrival; loop will add it and re-evaluate
                continue
        else:
            run_time = time_to_finish

        # Execute run_time (>=1)
        current_task.remaining -= run_time
        time += run_time
        current_task.end_times.append(time)

        # If finished, set completion and clear current_task
        if current_task.remaining == 0:
            current_task.completion = time
            current_task = None
        else:
            # current_task is preemptible: it stays as candidate; it will be re-added to ready in next loop if needed
            # we add it back to ready for future selection
            ready.append(current_task)
            current_task = None

    total_time = time
    cpu_util = ((total_time - idle_time) / total_time) * 100 if total_time > 0 else 0.0
    finalize_tasks(tasks)
    return gantt, cpu_util

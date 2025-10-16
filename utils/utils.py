# utils.py
# Shared utilities: Task class, helpers to compute metrics and display Gantt chart segments.

from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class Task:
    """
    Task representation shared across schedulers.
    name: task identifier
    burst: original burst (execution) time
    arrival: arrival time
    priority: lower value => higher priority (optional)
    deadline: optional deadline for real-time analysis
    """
    name: str
    burst: int
    arrival: int
    priority: int = 0
    deadline: Optional[int] = None

    # dynamic fields used during simulation (initialized)
    remaining: int = field(init=False)
    completion: Optional[int] = field(init=False, default=None)
    start_times: List[int] = field(init=False, default_factory=list)
    end_times:   List[int] = field(init=False, default_factory=list)
    waiting: Optional[int] = field(init=False, default=None)
    turnaround: Optional[int] = field(init=False, default=None)
    missed_deadline: bool = field(init=False, default=False)

    def __post_init__(self):
        self.remaining = self.burst

def finalize_tasks(tasks: List[Task]):
    """
    Fills waiting and turnaround times and deadline status (if deadline provided).
    This is called after the scheduler sets completion times for tasks.
    """
    for t in tasks:
        if t.completion is None:
            # if task never completed (shouldn't happen in our sims)
            t.turnaround = None
            t.waiting = None
            t.missed_deadline = True
        else:
            t.turnaround = t.completion - t.arrival
            t.waiting = t.turnaround - t.burst
            if t.deadline is not None and t.completion > t.deadline:
                t.missed_deadline = True
            else:
                t.missed_deadline = False

def gantt_to_segments(gantt_log: List[Tuple[int, str]]):
    """
    Convert a simple gantt log format [(start_time, task_name), ...]
    into segments [(start, end, name), ...] by scanning subsequent starts.
    The scheduler functions produce a log where each entry
    marks the start time of an execution window for a given task.
    """
    segments = []
    for i, (start, name) in enumerate(gantt_log):
        if i + 1 < len(gantt_log):
            end = gantt_log[i + 1][0]
        else:
            end = start + 1
        segments.append((start, end, name))
    return segments


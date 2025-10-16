# RTOS Scheduling Simulation (Software-Based)

Enables one to **understand, visualize, and compare** different CPU scheduling algorithms with proper Gantt Charts and Comparisons made amongst them to Best and Worst Algorithms according to the needs.
Includes the top 5 RTOS Scheduling Algorithms listed below.
---

## Features
- **CPU Scheduling Algorithms Implemented:**
  1. **FCFS (First-Come, First-Serve):** Tasks are executed in the order they arrive.
  2. **SJF Non-Preemptive (Shortest Job First):** The task with the smallest burst time is executed next. Once a task starts, it runs to completion.
  3. **SJF Preemptive (Shortest Remaining Time First):** Similar to SJF Non-Preemptive but can preempt the running task if a shorter task arrives.
  4. **Priority Preemptive Scheduling:** Tasks with higher priority (lower numeric value) are executed first. A running task can be preempted by a higher-priority task.
  5. **Round Robin (Time Quantum Scheduling):** Each task gets a fixed time slice (quantum). If it doesn't finish, it is placed at the back of the queue.

- **Task Representation:**  
  Uses a `Task` dataclass with fields:  
  `name`, `burst`, `arrival`, `priority`, `deadline`, plus dynamic fields for `remaining`, `completion`, `waiting`, `turnaround`, and `missed_deadline`.  
  This allows all schedulers to use a **single class based interface**.

- **Metrics Computed:**
  - **Waiting Time:** Time a task spends waiting in the ready queue.
  - **Turnaround Time:** Total time from arrival to completion.
  - **Deadline Misses:** Checks if tasks finish after their deadline.

- **Visualization:**  
  Gantt chart-style logs show principles like Context Switching, Overhead, Avergae TAT and Overall Performance Stats, making scheduling behavior easy to understand.

- **Comparative Analysis:**  
  Compare **all algorithms together** in terms of average waiting and turnaround time, both in **table** and **bar chart** format.


---


## 🔹 Installation & Usage
  ```bash
  git clone https://github.com/your-username/RTOS_Scheduler_Simulation.git
  cd RTOS_Scheduler_Simulation 
pip install matplotlib
python compare_all.py

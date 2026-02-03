from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
import threading
import time


@dataclass
class RoleDescriptor:
    name: str
    skills: List[str] = field(default_factory=list)
    max_parallel_jobs: int = 1
    preferred: bool = False
    weight: int = 1


Handler = Callable[[Dict[str, Any]], Optional[Dict[str, Any]]]


class RoleArbiter:
    def __init__(self):
        self._roles: List[RoleDescriptor] = []
        self._job_queue: List[Dict[str, Any]] = []
        self._queue_lock = threading.Lock()
        self._handlers: Dict[str, Handler] = {}
        self._executor_threads: List[threading.Thread] = []
        self._stop = threading.Event()
        self._activations: List[Dict[str, Any]] = []

    def add_role(self, role: RoleDescriptor):
        self._roles.append(role)

    def register_handler(self, role_name: str, handler: Handler):
        self._handlers[role_name] = handler

    def schedule_job(self, role_name: str, task_ctx: Dict[str, Any]):
        with self._queue_lock:
            self._job_queue.append({"role": role_name, "task": task_ctx})

    def start_executor(self, num_threads: int = 1):
        if self._executor_threads:
            return
        self._stop.clear()
        for _ in range(num_threads):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            self._executor_threads.append(t)
            t.start()

    def stop_executor(self):
        self._stop.set()
        for t in list(self._executor_threads):
            t.join(timeout=1)
        self._executor_threads = []

    def _worker_loop(self):
        while not self._stop.is_set():
            job = None
            with self._queue_lock:
                if self._job_queue:
                    job = self._job_queue.pop(0)
            if job is None:
                time.sleep(0.01)
                continue
            role = job.get('role')
            task = job.get('task') or {}
            self._activations.append({"role": role, "status": "running", "task": task})
            handler = self._handlers.get(role)
            try:
                if handler:
                    res = handler(task)
                    self._activations.append({"role": role, "status": res.get('status') if isinstance(res, dict) and 'status' in res else 'completed', 'task': task})
                else:
                    # fast simulated work
                    time.sleep(min(0.01, float(task.get('simulate_duration', 0))))
                    self._activations.append({"role": role, "status": "completed", "task": task})
            except Exception:
                self._activations.append({"role": role, "status": "failed", "task": task})

    def get_activations(self):
        return list(self._activations)

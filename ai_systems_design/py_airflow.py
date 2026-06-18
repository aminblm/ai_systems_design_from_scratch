import time

class AirflowDAG:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, name, default_args=None):
        self.name = name 
        self.default_args = default_args or {}
        self.tasks = []
        self.schedule_interval = None 

    def add_task(self, task, schedule=None, dependencies=None):
        task.name = task.name
        task.schedule = task.schedule or schedule
        task.dependencies = dependencies 
        self.tasks.append(task)

class Task:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, name, execute_func, schedule=None, dependencies=None):
        self.name = name
        self.execute_func = execute_func 
        self.schedule = schedule 
        self.dependencies = dependencies or {}

    def execute(self):
        print(f"Executing Task: {self.name}")
        # Simulate execution
        self.execute_func()
        return True 
    

class Scheduler:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, dag):
        self.dag = dag
        self.current_time = 0
        self.task_executions = {}

    def start(self):
        print("Scheduler started...")
        while True:
            self._check_schedules()
            self._execute_tasks()
            self.current_time += 1 # Simulate time passing

    def _check_schedules(self):
        for task in self.dag.tasks:
            if self._is_due(task):
                self._schedule_task(task)

    def _execute_tasks(self):
        for index, task in zip(range(len(self.dag.tasks)), self.dag.tasks):
            if self._is_due(task):
                task.execute()
                time.sleep(int(task.schedule.split(' ')[0]))

    def _is_due(self, task):
        if not task.schedule: return False 
        # Simple cron-like schedule (e.g. every 5 seconds)
        return self.current_time % (int(task.schedule.split(' ')[0]) if task.schedule else 1) == 0

    def _schedule_task(self, task):
        self.task_executions[task.name] = task 
        # Simulate scheduling (in real code, this would be handled by a scheduler)
        print(f'Task {task.name} scheduled')

if __name__ == "__main__":
    dag = AirflowDAG("Sample DAG")

    def my_task():
        # Simple Task
        print("Task executed!")

    task = Task("My Task", my_task, schedule="5 * * * *")

    dag.add_task(task)

    scheduler = Scheduler(dag)
    scheduler.start()
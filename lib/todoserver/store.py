class TaskStore:
    def __init__(self):
        self.tasks = dict()
    def get_all_tasks(self):
        return [
            { task_id: task["summary"] }
            for task_id, task in self.tasks.items()
        ]
    def create_task(self, summary, description):
        try:
            task_id = 1 + max(self.tasks.keys())
        except ValueError:
            task_id = 1
        self.tasks[task_id] = {
            "summary": summary,
            "description": description,
        }
        return task_id
    def task_details(self, task_id):
        task_info = self.tasks[task_id].copy()
        task_info["id"] = task_id
        return task_info

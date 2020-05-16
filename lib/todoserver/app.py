# ./lib/todoserver/app.py

from flask import Flask, make_response, request
import json


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



class TodoserverApp(Flask):
    def __init__(self, name):
        self.store = TaskStore()
        super().__init__(name)
    def erase_all_test_data(self):
        assert self.testing
        self.store.tasks.clear()
        


#app = Flask(__name__)
app = TodoserverApp(__name__)

# MEMORY = dict()

@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = [
        {"id": task_id, "summary": task["summary"]}
        for task_id, task in app.store.tasks.items()
    ]
    return make_response(json.dumps(tasks), 200)

@app.route("/tasks/", methods=["POST"])
def create_task():
    payload = request.get_json(force=True)

    try:
        task_id = 1 + max(app.store.tasks.keys())
    except ValueError:
        task_id = 1

    app.store.tasks[task_id] = {
        "summary": payload["summary"],
        "description": payload["description"],
    }
    task_info = {"id": task_id}
    return make_response(json.dumps(task_info), 201)

@app.route("/tasks/<int:task_id>/", methods=["GET"])
def get_task_details(task_id):
    task_info = app.store.tasks[task_id].copy()
    task_info["id"] = task_id
    return make_response(json.dumps(task_info), 200)

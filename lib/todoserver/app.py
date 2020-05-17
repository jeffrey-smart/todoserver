# ./lib/todoserver/app.py

from flask import Flask, make_response, request
import json
from .store import TaskStore

class TodoserverApp(Flask):
    def init_db(self, engine_spec):
        self.store = TaskStore(engine_spec)

    def erase_all_test_data(self):
        assert self.testing
        self.store._delete_all_tasks()



#app = Flask(__name__)
app = TodoserverApp(__name__)

# MEMORY = dict()

@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = app.store.get_all_tasks()
    return make_response(json.dumps(tasks), 200)

@app.route("/tasks/", methods=["POST"])
def create_task():
    payload = request.get_json(force=True)

    task_id = app.store.create_task(
        summary = payload["summary"],
        description = payload["description"],
    )
    task_info = {"id": task_id}
    return make_response(json.dumps(task_info), 201)

@app.route("/tasks/<int:task_id>/", methods=["GET"])
def get_task_details(task_id):
    task_info = app.store.task_details(task_id)
    return make_response(json.dumps(task_info), 200)

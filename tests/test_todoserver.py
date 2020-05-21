import json
import unittest
from todoserver import app #, MEMORY

app.testing = True
app.init_db("sqlite:///:memory:")

def json_body(resp):
    return json.loads(resp.data.decode("utf-8"))

class TestTodoserver(unittest.TestCase):
    def setUp(self):
        app.erase_all_test_data()

        self.client = app.test_client()
        resp = self.client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], json_body(resp))

    def test_get_empty_list_of_tasks(self):
        resp = self.client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], json_body(resp))

    def test_create_a_task_and_get_its_details(self):

        # verify creating a task
        new_task = {
            "summary": "Get milk", 
            "description": "One gallon of whole milk",
            }

        client = app.test_client()

        resp = client.post("/tasks/", data=json.dumps(new_task))
        task_id_from_post = json_body(resp).get("id")
        self.assertEqual(201, resp.status_code)
        data = json_body(resp)
        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertEqual(task_id_from_post, data["id"])

        # verify getting task details
        task_id = data["id"]

        resp = client.get(f"/tasks/{task_id:d}/")
        self.assertEqual(200, resp.status_code)
        data = json_body(resp)
        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertIn("summary", data)
        self.assertIn("description", data)

        self.assertEqual(task_id, data["id"])
        self.assertEqual("Get milk", data["summary"])
        self.assertEqual("One gallon of whole milk", 
                         data["description"])

    def test_create_multiple_tasks_and_retrieve_list(self):
        # create a list of tasks
        new_tasks = [
            {"summary": "Pick up milk", 
             "description": "Half gallon of almond milk", },
            {"summary": "Fix blog", 
             "description": "Check spelling of Tucson", },
            {"summary": "Get gas", 
             "description": "Put gas in van", },
        ]

        # post the list of tasks
        for new_task in new_tasks:
            with self.subTest(new_task=new_task):
                resp = self.client.post("/tasks/", 
                                        data=json.dumps(new_task))
                self.assertEqual(201, resp.status_code)
                data = json_body(resp)
                self.assertIsInstance(data, dict)
                self.assertIn("id", data)

        # retrieve the list of tasks
        resp = self.client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        tasks = json_body(resp)
        self.assertEqual(3, len(tasks))
        for actual, expected in zip(new_tasks, tasks):
            self.assertEqual(expected["summary"], actual["summary"])

    def test_error_when_getting_nonexistent_task(self):
        resp = self.client.get("/tasks/42/")
        self.assertEqual(404, resp.status_code)

    def test_delete_task(self):
        # create a task
        new_task_data = {
            "summary": "Pick up bottled water",
            "description": "Big green bottle of sparkling water",
        }
        resp = self.client.post("/tasks/",
                                data=json.dumps(new_task_data)
        )
        self.assertEqual(201, resp.status_code)
        task = json_body(resp)
        task_id = task["id"]

        # delete the task
        resp = self.client.delete(f"/tasks/{task_id:d}/")   
        self.assertEqual(200, resp.status_code)

        # verify that task has been deleted
        resp = self.client.get(f"/tasks/{task_id:d}/")
        self.assertEqual(404, resp.status_code)

    def test_error_when_deleting_nonexistent_task(self):
        # delete the task
        resp = self.client.delete(f"/tasks/42/")   
        self.assertEqual(404, resp.status_code)
    
    def test_modify_existing_task(self):
        # create a task
        new_task_data = {
            "summary": "Pick up bottled water",
            "description": "Big green bottle of sparkling water",
        }
        resp = self.client.post("/tasks/",
                                data=json.dumps(new_task_data)
        )
        self.assertEqual(201, resp.status_code)
        task = json_body(resp)
        task_id = task["id"]

        # modify (update) the task
        updated_task_data = {
            "summary": "Put air in tires",
            "description": "Inflate to 35 psi",
        }
        resp = self.client.put(f"/tasks/{task_id:d}/",
                               data = json.dumps(updated_task_data))
        self.assertEqual(200, resp.status_code)

        # check the task -- did we really modify it?
        resp = self.client.get(f"/tasks/{task_id:d}/")
        self.assertEqual(200, resp.status_code)
        
        actual = json_body(resp)
        self.assertEqual(updated_task_data["summary"], actual["summary"])
        self.assertEqual(updated_task_data["description"], actual["description"])

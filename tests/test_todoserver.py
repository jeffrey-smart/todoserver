import json
import unittest

# pylint: disable=import-error
from todoserver import app #, MEMORY
# pylint: enable=import-error

app.testing = True
app.init_db("sqlite:///:memory:")

def json_body(resp):
    return json.loads(resp.data.decode("utf-8"))


class TestTodoserver(unittest.TestCase):
    def create_test_task(self):
        new_task_data = {
            "summary": "Pick up bottled water",
            "description": "Big green bottle of sparkling water",
        }
        resp = self.client.post("/tasks/", data=json.dumps(new_task_data))
        assert resp.status_code == 201, print(resp.status_code)
        assert "id" in json_body(resp), print(json_body(resp))
        return json_body(resp)

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

        data = self.create_test_task()

        # verify getting task details
        task_id = data["id"]

        resp = self.client.get(f"/tasks/{task_id:d}/")
        self.assertEqual(200, resp.status_code)
        data = json_body(resp)
        self.assertIsInstance(data, dict)
        self.assertIn("id", data)
        self.assertIn("summary", data)
        self.assertIn("description", data)

        self.assertEqual(task_id, data["id"])
        self.assertEqual("Pick up bottled water", data["summary"])
        self.assertEqual("Big green bottle of sparkling water", data["description"])

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
                resp = self.client.post("/tasks/", data=json.dumps(new_task))
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
        task = self.create_test_task()
        task_id = task["id"]

        # delete the task
        resp = self.client.delete(f"/tasks/{task_id:d}/")   
        self.assertEqual(200, resp.status_code)

        # verify that task has been deleted
        resp = self.client.get(f"/tasks/{task_id:d}/")
        self.assertEqual(404, resp.status_code)

    def test_error_when_deleting_nonexistent_task(self):
        # delete the task
        resp = self.client.delete("/tasks/42/")   
        self.assertEqual(404, resp.status_code)
    
    def test_modify_existing_task(self):
        # create a task
        task = self.create_test_task()
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

    def test_error_when_updating_non_existent_task(self):
        # modified (revised) version of the task
        # modify (update) the task
        updated_task_data = {
            "summary": "Get gas",
            "description": "Fill up with unleaded",
        }
        resp = self.client.put("/tasks/42/",
                               data = json.dumps(updated_task_data))
        self.assertEqual(404, resp.status_code)

    def test_error_when_creating_task_with_bad_summary(self):
        bad_summaries = [
            "?" * 120,                  # too long
            "Goodby \n Columbus",       # embedded newline
        ]
        for bad_summary in bad_summaries:
            task_info = { "summary": bad_summary,
                          "description": "", }
                          
            with self.subTest(bad_summary=bad_summary):
                resp = self.client.post("/tasks/", data=json.dumps(task_info))
                self.assertEqual(400, resp.status_code)
                task_info = json_body(resp)
                self.assertIn("error", task_info)
                self.assertEqual(
                    "Summary must be under 120 chars, without newlines",
                    task_info["error"]
                )

    def test_error_when_updating_task_with_bad_summary(self):
        task = self.create_test_task()
        task_id = task["id"]

        bad_summaries = [
            "?" * 120,                  # too long
            "Goodby \n Columbus",       # embedded newline
        ]
        for bad_summary in bad_summaries:
            updated_task_data = { "summary": bad_summary,
                                  "description": "", }
                          
            with self.subTest(bad_summary=bad_summary):
                resp = self.client.put(
                    f"/tasks/{task_id:d}/",
                    data = json.dumps(updated_task_data)
                )
                self.assertEqual(400, resp.status_code)

                task_info = json_body(resp)
                self.assertIn("error", task_info)
                self.assertEqual(
                    "Summary must be under 120 chars, without newlines",
                    task_info["error"]
                )

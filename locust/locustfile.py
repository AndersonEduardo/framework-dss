import random
from locust import HttpUser, task, between, SequentialTaskSet


class UserBehavior(SequentialTaskSet):

    @task
    def api_autocomplete_category(self):

        query_data = {
                        "decision_tree_name": "obesity-ldt",
                        "context": "pc-bra",
                        "parameters": {
                            "cid-10": "E66",
                            "imc": random.randint(15, 55),
                            "time-under-clinical-protocols": random.randint(0, 3),
                            "comorbidities": "true"
                        }
                    }

        self.client.post("/query", json=query_data)


class WebsiteUser(HttpUser):

   tasks = [UserBehavior]
   wait_time = between(1, 5)
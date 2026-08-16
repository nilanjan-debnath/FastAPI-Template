from locust import HttpUser, task, between


class HelloWorldUser(HttpUser):
    # waiting time to visiting another endpoint
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/healthz")


# run command: uv run locust -f tests/load-testing.py

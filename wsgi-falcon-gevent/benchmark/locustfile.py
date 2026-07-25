from locust import HttpUser, task


class BenchmarkUser(HttpUser):
    host = "https://wsgi-falcon-gevent.0a.com.ar"

    @task
    def plain(self):
        self.client.get("/plain")

    # @task
    # def json_1(self):
    #     self.client.get("/json-1")

    # @task
    # def json_2(self):
    #     self.client.get("/json-2")

    # @task
    # def cpu_1(self):
    #     self.client.get("/cpu-1")

    # @task
    # def cpu_2(self):
    #     self.client.get("/cpu-2")

    # @task
    # def io_1(self):
    #     self.client.get("/io-1")

    # @task
    # def io_2(self):
    #     self.client.get("/io-2")

    # @task
    # def http_1(self):
    #     self.client.get("/http-1")

    # @task
    # def http_2(self):
    #     self.client.get("/http-2")

    # @task
    # def hash_1(self):
    #     self.client.get("/hash-1")

    # @task
    # def hash_2(self):
    #     self.client.get("/hash-2")

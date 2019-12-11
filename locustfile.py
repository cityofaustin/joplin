from locust import HttpLocust, TaskSet, task, between


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        # login to the application
        response = self.client.get('/admin/login/')
        csrftoken = response.cookies['csrftoken']
        self.client.post('/admin/login/',
                         {"email": "admin@austintexas.io", "password": "x"},
                         headers={'X-CSRFToken': csrftoken})

    def logout(self):
        self.client.post("/admin/logout", {"email": "admin@austintexas.io", "password": "x"})

    @task(2)
    def index(self):
        self.client.get("/admin/pages/search/")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)

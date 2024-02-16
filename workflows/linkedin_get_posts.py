from workflows.linkedin_workflow import LinkedinWorkflow, LinkedinAuth


class LinkedinGetPosts(LinkedinWorkflow):
    def __init__(self) -> None:
        self.auth = LinkedinAuth()
        super().__init__()

    def execute(self, *args, **kwargs):
        driver_key = self.open_browser()
        self.login(driver_key, username=self.auth.username, password=self.auth.password)

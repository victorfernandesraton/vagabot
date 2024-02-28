from vagabot.workflows.linkedin_auth import LinkedinAuth
import numpy as np
from decouple import config
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions
import selenium.webdriver.support.expected_conditions as EC


class LinkedinCommentPost(LinkedinAuth):
    AUTHOR_PLACEHOLDER = "__author__"
    COMMENT_BUTTON_SELECTOR = "div.editor-content div.ql-editor"
    SEND_COMMENT_BUTTON_SELECTOR = "button.comments-comment-box__submit-button"

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def _replace_message(self, post: dict) -> str:
        return self.message.replace(self.AUTHOR_PLACEHOLDER, post["author"]["name"])

    def multiprocess_task(self, posts: list):
        chunk_size = config("CONCURRENT_TASKS", 2)
        if len(self.posts) < chunk_size:
            chunk_size = 1
        posts_to_proccess = np.split(np.array(posts), chunk_size)
        with ThreadPoolExecutor(max_workers=chunk_size) as executor:
            for chunk in posts_to_proccess:
                executor.submit(self.execute, [chunk])

    def execute(self, posts: list, username: str, password: str):
        driver_key = self.open_browser()
        self.login(self.drivers[driver_key], username, password)

        input_wait = WebDriverWait(self.drivers[driver_key], timeout=20)
        for post in posts:
            self.drivers[driver_key].get(post["post"]["link"])
            try:
                btn_comment = input_wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.COMMENT_BUTTON_SELECTOR)
                    )
                )
                ActionChains(self.drivers[driver_key]).move_to_element(
                    btn_comment
                ).click().perform()
                btn_comment.send_keys(self._replace_message(post))
            except exceptions.TimeoutException:
                raise Exception("Not found button for comment")

            try:
                btn_send_comment = input_wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.SEND_COMMENT_BUTTON_SELECTOR)
                    )
                )
                btn_send_comment.click()
            except exceptions.TimeoutException:
                raise Exception("Not found button for submit comment")

        self.close(driver_key)

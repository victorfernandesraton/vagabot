from concurrent.futures import ThreadPoolExecutor
from typing import List

import numpy as np
import selenium.webdriver.support.expected_conditions as EC
from decouple import config
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from vagabot.entities import Post, PostStatus
from vagabot.workflows.linkedin_auth import LinkedinAuth
from vagabot.repository.post_repository import PostRepository


class LinkedinCommentPost(LinkedinAuth):
    AUTHOR_PLACEHOLDER = "__author__"
    COMMENT_BUTTON_SELECTOR = "div.editor-content div.ql-editor"
    SEND_COMMENT_BUTTON_SELECTOR = "button.comments-comment-box__submit-button"

    def __init__(self, message: str, post_repository: PostRepository) -> None:
        super().__init__()
        self.message = message
        self.post_repository = post_repository

    def multiprocess_task(self, posts: List[Post]):
        chunk_size = config("CONCURRENT_TASKS", 2)
        if len(self.posts) < chunk_size:
            chunk_size = 1
        posts_to_proccess = np.split(np.array(posts), chunk_size)
        with ThreadPoolExecutor(max_workers=chunk_size) as executor:
            for chunk in posts_to_proccess:
                executor.submit(self.execute, [chunk])

    def execute(self, posts: List[Post], username: str, password: str):
        driver_key = self.open_browser()
        self.login(self.drivers[driver_key], username, password)
        result = []

        input_wait = WebDriverWait(self.drivers[driver_key], timeout=20)
        for post in posts:
            self.drivers[driver_key].get(post.link)
            try:
                btn_comment = input_wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.COMMENT_BUTTON_SELECTOR)
                    )
                )
                ActionChains(self.drivers[driver_key]).move_to_element(
                    btn_comment
                ).click().perform()
                btn_comment.send_keys(self.message)
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

            # TODO: Move this for event emmiter
            updated_post = Post(
                linkedin_id=post.linkedin_id,
                link=post.link,
                author_id=post.author_id,
                content=post.content,
                id=post.id,
                status=PostStatus.COMMENTED,
            )
            self.post_repository.upsert_by_linkedin_id(updated_post)
        self.close(driver_key)

from typing import List

import selenium.webdriver.support.expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from vagabot.entities import Post, PostStatus
from vagabot.repository.post_repository import PostRepository

from .linkedin_workflow import LinkedinWorkflow


class LinkedinCommentPost(LinkedinWorkflow):
    AUTHOR_PLACEHOLDER = "__author__"
    COMMENT_BUTTON_SELECTOR = "div.editor-content div.ql-editor"
    SEND_COMMENT_BUTTON_SELECTOR = "button.comments-comment-box__submit-button"

    def __init__(
        self, *args, message: str, post_repository: PostRepository, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.message = message
        self.post_repository = post_repository

    def execute(self, posts: List[Post], driver_key: str):
        self.browser_service.drivers[driver_key].get("https://www.linkedin.com")
        input_wait = WebDriverWait(self.browser_service.drivers[driver_key], timeout=20)
        for post in posts:
            self.browser_service.drivers[driver_key].get(post.link)
            try:
                btn_comment = input_wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.COMMENT_BUTTON_SELECTOR)
                    )
                )
                ActionChains(self.browser_service.drivers[driver_key]).move_to_element(
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

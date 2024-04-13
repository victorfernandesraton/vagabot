import time
from abc import abstractmethod

from selenium.webdriver.remote.webelement import WebElement

from vagabot.services import BrowserService


class LinkedinWorkflow:
    def __init__(self, browser_service: BrowserService) -> None:
        self.browser_service = browser_service

    @staticmethod
    def human_input_simulate(element: WebElement, content: str, delay=1):
        for key in content:
            time.sleep(delay)
            element.send_keys(key)

    @abstractmethod
    def execute(self, *args, **kwargs): ...

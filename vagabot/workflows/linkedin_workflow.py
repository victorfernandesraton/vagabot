import time
from abc import abstractmethod

import fake_useragent
from decouple import config
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from undetected_chromedriver import ChromeOptions


class LinkedinWorkflow:
    _username = config("LINKEDIN_EMAIL")
    _password = config("LINKEDIN_PASS")

    def __init__(self) -> None:
        self.drivers: dict[str, WebDriver] = {}

    @staticmethod
    def human_input_simulate(element: WebElement, content: str, delay=1):
        for key in content:
            time.sleep(delay)
            element.send_keys(key)

    def open_browser(self) -> str:
        opts = ChromeOptions()
        opts.add_argument(
            f"user-agent={fake_useragent.UserAgent(os='windows', browsers=['chrommiun'])}"
        )
        driver = webdriver.Remote(options=opts)

        if not driver.session_id:
            raise Exception("Not able to regisrer a driver")
        driver.maximize_window()
        self.drivers[driver.session_id] = driver

        return driver.session_id

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...

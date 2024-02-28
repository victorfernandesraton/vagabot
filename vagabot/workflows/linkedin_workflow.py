import time
from abc import abstractmethod

import fake_useragent
from decouple import config
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from undetected_chromedriver import ChromeOptions


class LinkedinWorkflow:
    # TODO: moving foward for cli
    _se_router_host = config("SE_ROUTER_HOST", "localhost")
    _se_router_port = config("SE_ROUTER_PORT", "4444")

    def __init__(self) -> None:
        self.drivers: dict[str, WebDriver] = {}
        if self._se_router_port:
            self._se_router_url = (
                f"http://{self._se_router_host}:{self._se_router_port}"
            )
        else:
            self._se_router_url = f"http://{self._se_router_host}"

    @staticmethod
    def human_input_simulate(element: WebElement, content: str, delay=1):
        for key in content:
            time.sleep(delay)
            element.send_keys(key)

    def open_browser(self) -> str:
        print(f"Open browser in {self._se_router_url}")
        opts = ChromeOptions()
        opts.add_argument(
            f"user-agent={fake_useragent.UserAgent(os='windows', browsers=['chrommiun'])}"
        )
        driver = webdriver.Remote(options=opts, command_executor=self._se_router_url)

        if not driver.session_id:
            raise Exception("Not able to regisrer a driver")
        driver.maximize_window()
        self.drivers[driver.session_id] = driver

        return driver.session_id

    def close(self, driver_key: str):
        self.drivers[driver_key].close()
        del self.drivers[driver_key]

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...

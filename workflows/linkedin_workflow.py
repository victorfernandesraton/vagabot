from abc import abstractmethod
import logging
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from decouple import config
from undetected_chromedriver import ChromeOptions
import fake_useragent


class LinkedinWorkflow:
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

    def login(self, driver_key: str, username: str, password: str):
        driver = self.drivers[driver_key]
        logging.info("go to site")
        driver.maximize_window()
        driver.get("https://www.linkedin.com")
        input_wait = WebDriverWait(self.drivers[driver_key], timeout=30)
        logging.info("set input")
        try:
            email_input = input_wait.until(
                EC.presence_of_element_located((By.ID, "session_key"))
            )
            self.human_input_simulate(email_input, username)
        except TimeoutException:
            logging.info("Not found login input")

        try:
            pass_input = input_wait.until(
                EC.presence_of_element_located((By.ID, "session_password"))
            )
            self.human_input_simulate(pass_input, password)
        except TimeoutException:
            logging.info("Not found pass input")

        try:
            btn_submit = input_wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
            )
            btn_submit.click()
        except TimeoutException:
            logging.info("Not found button input")
        finally:
            logging.info("button clicked")

    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class LinkedinAuth:
    def __init__(self):
        self.username = config("LINKEDIN_EMAIL")
        self.password = config("LINKEDIN_PASS")

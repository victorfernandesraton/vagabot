import logging
import time
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from vagabot.workflows.linkedin_workflow import LinkedinWorkflow


class LinkedinAuth(LinkedinWorkflow):
    USERNAME_INPUT_XPATH = "//input[@id='session_key']"
    PASSWORD_INPUT_XPATH = "//input[@id='session_password']"
    BUTTON_SUBMIT_XPATH = "//*[@id='main-content']/section/div/div/form/div/button"

    def execute(self, driver: WebDriver, username: str, password: str):
        logging.info("go to site")
        driver.maximize_window()
        driver.get("https://www.linkedin.com")
        input_wait = WebDriverWait(driver, timeout=30)
        logging.info("set input")
        input_list = {
            self.USERNAME_INPUT_XPATH: username,
            self.PASSWORD_INPUT_XPATH: password,
        }
        for xpath, value in input_list.items():
            try:
                txt_input = input_wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                self.human_input_simulate(txt_input, value)
            except exceptions.TimeoutException:
                raise Exception(f"Not found {xpath} input")

        try:
            time.sleep(5)
            btn_submit = input_wait.until(
                EC.presence_of_element_located((By.XPATH, self.BUTTON_SUBMIT_XPATH))
            )

            btn_submit.click()
            logging.info("button clicked")
        except exceptions.TimeoutException:
            raise Exception("Not found button input")

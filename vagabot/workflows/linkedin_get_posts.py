import time
from enum import Enum
from typing import List

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .linkedin_workflow import LinkedinWorkflow


class DatePostOptions(Enum):
    LAST_24_HOURS = "datePosted-past-24h"
    LAST_WEEK = "datePosted-past-week"
    LAST_MONTH = "datePosted-past-month"


class LinkedinGetPosts(LinkedinWorkflow):
    SEARCH_INPUT_XPATH = "//*[@id='global-nav-typeahead']/input"
    POSTS_BUTTON_SELECT = (
        "/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[2]/button"
    )
    POSTS_LIST_XPATH = "//ul[@role='list' and contains(@class, 'reusable-search__entity-result-list ')]/li"

    def execute(
        self,
        driver_key: str,
        queue_search: str,
        filters: dict = {},
    ) -> List[str | None]:
        self.browser_service.drivers[driver_key].get("https://www.linkedin.com")
        input_wait = WebDriverWait(self.browser_service.drivers[driver_key], timeout=20)
        try:
            search_input = input_wait.until(
                EC.presence_of_element_located((By.XPATH, self.SEARCH_INPUT_XPATH))
            )
            self.human_input_simulate(search_input, queue_search)
            self.human_input_simulate(search_input, Keys.ENTER)
        except exceptions.TimeoutException:
            raise Exception("not found input here search")

        self.browser_service.drivers[driver_key].get(
            f"https://www.linkedin.com/search/results/content/?keywords={queue_search}&origin=SWITCH_SEARCH_VERTICAL&sid=r01"
        )
        time.sleep(5)
        print(filters)
        filter_by_date = filters.get("datePosted", None)
        if filter_by_date:
            self.__filter_by_post_date(driver_key, DatePostOptions[filter_by_date])

        try:
            post_list = input_wait.until(
                EC.presence_of_all_elements_located((By.XPATH, self.POSTS_LIST_XPATH))
            )[:9]

        except exceptions.TimeoutException:
            raise Exception("not found post list")

        result = [post.get_attribute("outerHTML") for post in post_list]
        return result

    # TODO: Make this generic for all filter later
    def __filter_by_post_date(self, driver_key: str, option: DatePostOptions):
        input_wait = WebDriverWait(self.browser_service.drivers[driver_key], timeout=20)
        try:
            filter_button = input_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//button[@id='searchFilter_datePosted']")
                )
            )
            filter_button.click()
        except (exceptions.TimeoutException, exceptions.NoSuchElementException):
            raise Exception("not found sort by date filter")

        try:
            option_radio = input_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//input[@id='{option.value}']/../label")
                )
            )
            option_radio.click()
        except (exceptions.TimeoutException, exceptions.NoSuchElementException):
            raise Exception("not found sort by date filter")

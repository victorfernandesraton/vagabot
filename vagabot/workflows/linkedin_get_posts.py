import logging
import time
from enum import Enum
from typing import List
from urllib.parse import ParseResult, parse_qs, parse_qsl, urlencode, urlparse

from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .linkedin_workflow import LinkedinWorkflow


class DatePostOptions(Enum):
    LAST_24_HOURS = "past-24h"
    LAST_WEEK = "past-week"
    LAST_MONTH = "past-month"


filterOptions = {"datePosted": DatePostOptions}


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
        except exceptions.TimeoutException as e:
            logging.error("not found input here search")
            raise Exception(e)

        url = self.__get_current_url(driver_key)
        query = parse_qs(url.query)
        query.update(self.__create_filter_url(driver_key, filters))
        query.update({"keywords": queue_search})
        updated_url = url._replace(
            query=urlencode(query, doseq=True), path="search/results/content/"
        )
        self.browser_service.drivers[driver_key].get(updated_url.geturl())
        time.sleep(5)

        try:
            post_list = input_wait.until(
                EC.presence_of_all_elements_located((By.XPATH, self.POSTS_LIST_XPATH))
            )[:9]

        except exceptions.TimeoutException as e:
            logging.error("not found post list")
            raise Exception(e)

        result = [post.get_attribute("outerHTML") for post in post_list]
        logging.info(f"Found {len(result)} avaliable posts")
        return result

    def __get_current_url(self, driver_key: str) -> ParseResult:
        url_str = self.browser_service.drivers[driver_key].current_url
        url = urlparse(url_str)
        return url

    def __create_filter_url(self, driver_key: str, filter: dict):
        result = {}
        for key, value in filter.items():
            enum_filter = filterOptions.get(key, None)
            if enum_filter:
                result[key] = enum_filter[value].value

        return result

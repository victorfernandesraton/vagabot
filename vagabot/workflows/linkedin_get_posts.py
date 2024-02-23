from vagabot.workflows.linkedin_auth import LinkedinAuth
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from typing import List


class LinkedinGetPosts(LinkedinAuth):
    SEARCH_INPUT_XPATH = "//*[@id='global-nav-typeahead']/input"
    POSTS_BUTTON_SELECT = (
        "/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[2]/button"
    )
    POSTS_LIST_XPATH = "//div[@class='scaffold-finite-scroll__content']/div/div/ul/li"

    def execute(self, queue_search: str) -> List[str]:
        result = []
        driver_key = self.open_browser()
        self.login(
            self.drivers[driver_key], username=self._username, password=self._password
        )
        input_wait = WebDriverWait(self.drivers[driver_key], timeout=20)
        try:
            search_input = input_wait.until(
                EC.presence_of_element_located((By.XPATH, self.SEARCH_INPUT_XPATH))
            )
            self.human_input_simulate(search_input, queue_search)
            self.human_input_simulate(search_input, Keys.ENTER)
        except exceptions.TimeoutException:
            raise Exception("not found input here search")

        self.drivers[driver_key].get(
            f"https://www.linkedin.com/search/results/content/?keywords={queue_search}&origin=SWITCH_SEARCH_VERTICAL&sid=r01"
        )

        try:
            post_list = input_wait.until(
                EC.presence_of_all_elements_located((By.XPATH, self.POSTS_LIST_XPATH))
            )[:9]

            result = [post.get_attribute("outerHTML") for post in post_list]

        except exceptions.TimeoutException:
            raise Exception("not found post list")

        return result

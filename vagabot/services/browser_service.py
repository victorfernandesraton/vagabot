import logging

import fake_useragent
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from undetected_chromedriver import ChromeOptions


class BrowserService:
    _se_router_host = ""
    _se_router_port: str | int = 4444

    def __init__(self, se_router_host: str, se_router_port: str | int) -> None:
        self._se_router_host = se_router_host
        self._se_router_port = se_router_port
        self.drivers: dict[str, WebDriver] = {}
        if self._se_router_port:
            self._se_router_url = (
                f"http://{self._se_router_host}:{self._se_router_port}"
            )
        else:
            self._se_router_url = f"http://{self._se_router_host}"

    def __create_driver(self) -> WebDriver:
        opts = ChromeOptions()
        opts.add_argument(
            f"user-agent={fake_useragent.UserAgent(os='windows', browsers=['chrommiun'])}"
        )
        driver = webdriver.Remote(options=opts, command_executor=self._se_router_url)
        return driver

    def open_browser(self) -> str:
        logging.debug(f"Open browser in {self._se_router_url}")
        driver = self.__create_driver()

        if not driver.session_id:
            raise Exception("Not able to regisrer a driver")
        driver.maximize_window()
        self.drivers[driver.session_id] = driver

        return driver.session_id

    def close(self, driver_key: str):
        self.drivers[driver_key].close()
        del self.drivers[driver_key]

    def __del__(self):
        for session_id, driver in self.drivers.items():
            try:
                driver.quit()
                logging.debug(f"Closed driver with session_id {session_id}")
            except Exception as e:
                logging.error(f"Error when close driver {session_id}: {e}")
            finally:
                try:
                    if session_id:
                        logging.error(
                            f"Derrubando o driver com session_id {session_id} do Selenium Grid."
                        )
                        webdriver.Remote(
                            command_executor=driver.command_executor,
                        ).quit()
                except Exception as e:
                    logging.error(
                        f"Erro ao desconectar o driver com session_id {session_id} do Selenium Grid: {e}"
                    )

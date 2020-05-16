import typing
import selenium
import logging
from selenium.webdriver import Chrome
import constants

logger = logging.getLogger(__name__)


class LoginCredentials(typing.NamedTuple):
    username: str
    password: str

    def __repr__(self):
        return "LoginCredentials(<username>, <password>)"

    def __str__(self):
        return repr(self)


class Session:
    _USERNAME_INPUT_XPATH = constants.USERNAME_INPUT_XPATH
    _PWD_INPUT_XPATH = constants.PWD_INPUT_XPATH

    def __init__(self, login_credentials: LoginCredentials):
        self.__login_credentials = login_credentials
        self.browser = Chrome("./chromedriver.exe")
        self.browser.implicitly_wait(3)

    def __enter__(self) -> selenium.webdriver.remote.webdriver.WebDriver:
        self.browser.get(constants.INSTAGRAM_URL)

        return self._login()

    def __exit__(self, *exc):
        if any(exc):
            logger.error(exc)

        self._logout()

    def _login(self) -> selenium.webdriver.remote.webdriver.WebDriver:
        username_textbox = self.browser.find_element_by_xpath(
            self._USERNAME_INPUT_XPATH
        )
        username_textbox.send_keys(self.__login_credentials.username)

        password_textbox = self.browser.find_element_by_xpath(self._PWD_INPUT_XPATH)
        password_textbox.send_keys(self.__login_credentials.password)

        password_textbox.submit()

        return self.browser

    def _logout(self):
        self.browser.close()

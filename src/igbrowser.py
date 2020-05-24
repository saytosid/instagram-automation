import constants

import logging
import time
import random
import typing
from enum import Enum
import selenium.webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


logger = logging.getLogger(__name__)

_XPATHS = constants.XPATHS


class Action(Enum):
    LIKE = "like"
    UNLIKE = "unlike"
    COMMENT = "comment"


class ActionNotSupported(Exception):
    ...


class LoginCredentials(typing.NamedTuple):
    username: str
    password: str

    def __repr__(self):
        return "LoginCredentials(<username>, <password>)"

    def __str__(self):
        return repr(self)


def rand_sleep(func):
    def decorated(*args, **kwargs):
        func(*args, **kwargs)
        time.sleep(random.random() * 2)

    return decorated


class Post:
    def __init__(
        self, container: selenium.webdriver.remote.webelement.WebElement, browser
    ):
        self.container = container
        self.browser = browser
        self._action_dispatcher = {
            Action.LIKE: self.like,
            Action.UNLIKE: self.unlike,
        }

    def perform_action(self, action: Action, *args, **kwargs):
        try:
            self._action_dispatcher[action](*args, **kwargs)
        except KeyError:
            raise ActionNotSupported

    @property
    def content(self):
        ...

    def _scroll_to_and_click(self, button):
        ActionChains(self.browser).move_to_element(button).click(button).perform()

    @rand_sleep
    def like(self):
        button = self.container.find_element(By.XPATH, _XPATHS["like_unlike_button"])
        if button.get_attribute("aria-label") == "Like":
            self._scroll_to_and_click(button)

    @rand_sleep
    def unlike(self):
        button = self.container.find_element(By.XPATH, _XPATHS["like_unlike_button"])
        if button.get_attribute("aria-label") == "Unlike":
            self._scroll_to_and_click(button)

    def comment(self, comment):
        raise NotImplementedError

    def get_comments(self) -> typing.Iterable[str]:
        raise NotImplementedError


class IGBrowser:
    def __init__(
        self, browser: selenium.webdriver.remote.webdriver.WebDriver,
    ):
        self.browser = browser
        self.browser.get(constants.INSTAGRAM_URL)
        self._handle_notification_button()

    def get_element(self, identifier, by=By.XPATH):
        return self.browser.find_element(by, identifier)

    def get_elements(self, identifier, by=By.XPATH):
        return self.browser.find_elements(by, identifier)

    def get_posts(self) -> typing.Iterable[Post]:
        post_path = _XPATHS["post_div_format"]
        while True:
            try:
                yield from (
                    Post(self.get_element(post_path.format(i)), self.browser)
                    for i in range(1, 100)
                )  # TODO: Return Post object
            except NoSuchElementException:
                self.scroll(2)

    @rand_sleep
    def scroll(self, num):
        actions = ActionChains(self.browser)
        for _ in range(num):
            actions.send_keys(Keys.SPACE).perform()

    def _handle_notification_button(self):
        try:
            notfication = self.get_element(_XPATHS["notifications_not_now_button"])
        except NoSuchElementException:
            pass
        else:
            notfication.click()

    def login(self, login_credentials: LoginCredentials):
        self.browser.get(constants.INSTAGRAM_URL)
        self.get_element(_XPATHS["username_field"]).send_keys(
            login_credentials.username
        )

        password_textbox = self.get_element(_XPATHS["password_field"])
        password_textbox.send_keys(login_credentials.password)
        password_textbox.submit()
        self._handle_notification_button()

    @property
    def logged_in(self):
        try:
            self.get_element(_XPATHS["my_profile_link"])
        except NoSuchElementException:
            return False
        else:
            return True

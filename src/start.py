#!/usr/bin/env python
from igbrowser import IGBrowser, LoginCredentials, Action
import constants
from selenium.webdriver import Chrome, ChromeOptions
import random
import logging


logger = logging.getLogger(__name__)


class ProbabilisticActionFilter:
    def __init__(self, probability_success: float):
        self.probability_success = probability_success

    def __call__(self) -> bool:
        return random.random() < self.probability_success


class Controller:
    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--user-data-dir=.user-data")
        options.add_argument("--profile-directory=.profile")

        self.browser = Chrome("./chromedriver.exe", options=options)
        self.browser.implicitly_wait(3)

    def run(self):
        ig_browser = IGBrowser(self.browser)
        if not ig_browser.logged_in:
            ig_browser.login(LoginCredentials(*constants.USERNAME_PWD))

        action_filter = ProbabilisticActionFilter(0.8)
        for post in ig_browser.get_posts():
            if action_filter():
                post.perform_action(Action.LIKE)


if __name__ == "__main__":
    Controller().run()

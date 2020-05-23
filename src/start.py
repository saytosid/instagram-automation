#!/usr/bin/env python
import actionfilter
from igbrowser import IGBrowser, LoginCredentials, Action, Post

import logging
import click
import json
from selenium.webdriver import Chrome, ChromeOptions
from typing import TextIO, Dict, NamedTuple, Iterable
from collections import defaultdict


logger = logging.getLogger(__name__)


class Controller:
    def __init__(
        self, login_credentials: LoginCredentials, actions: Dict, webdriver_path: str
    ):
        options = ChromeOptions()
        options.add_argument("--user-data-dir=.user-data")
        options.add_argument("--profile-directory=.profile")

        self.browser = Chrome(webdriver_path, options=options)
        self.browser.implicitly_wait(3)

        self.__login_credentials = login_credentials
        self.actions = actions

    def run(self):
        ig_browser = IGBrowser(self.browser)
        if not ig_browser.logged_in:
            ig_browser.login(self.__login_credentials)

        for post in ig_browser.get_posts():
            for (action, filter_group) in self.actions[Post]:
                if filter_group():
                    post.perform_action(action)


class ActionConfig(NamedTuple):
    action: Action
    filters: actionfilter.FilterGroup


def config_file_parser(config_file):
    config_dict = json.load(config_file)
    login_credentials = LoginCredentials(
        config_dict["username"], config_dict["password"]
    )
    webdriver_path = config_dict["webdriverPath"]

    actions = defaultdict(list)
    for resource_str, actions_json in config_dict["actions"].items():
        resource_type = _get_resource_type(resource_str)
        for action_config_json in actions_json:
            action = Action(action_config_json["actionName"])
            filter_group = _get_filter_group(action_config_json["filters"])
            actions[resource_type].append(ActionConfig(action, filter_group))

    return login_credentials, actions, webdriver_path


def _get_filter_group(filters_config: Iterable):
    return actionfilter.FilterGroup(
        filters=[
            getattr(actionfilter, f_cfg["filterName"])(**f_cfg["params"])
            for f_cfg in filters_config
        ]
    )


def _get_resource_type(resource: str):
    return {"post": Post}[resource]


@click.command()
@click.option(
    "--config-file", "-c", help="Path to config file", required=True, type=click.File()
)
def cli(config_file: TextIO):
    Controller(*config_file_parser(config_file)).run()


if __name__ == "__main__":
    cli()

import pytest
import unittest
import io
from unittest.mock import Mock, patch, MagicMock
from start import Controller, config_file_parser, LoginCredentials
from start import Post, Action, ActionConfig, actionfilter


class TestContoller:
    @pytest.fixture
    def mocks(self):
        login_credentials = Mock()
        browser = Mock()
        action = MagicMock()
        filter_group = MagicMock()
        actions = {Post: [(action, filter_group)]}
        controller = Controller(login_credentials, actions, browser)
        yield controller, login_credentials, action, filter_group

    @pytest.fixture
    def ig_browser_mock(self, mocks):
        ig_browser_type = MagicMock()
        ig_browser = ig_browser_type.return_value
        ig_browser.get_posts.return_value = []
        yield ig_browser_type, ig_browser

    class TestLoginFunctinailty:
        def test_controller_logged_in_ok(self, mocks, ig_browser_mock):
            # GIVEN
            ig_browser_type, ig_browser = ig_browser_mock
            controller, login_credentials, _, _ = mocks
            ig_browser.logged_in = True

            # WHEN
            Controller.run(controller, igbrowser_type=ig_browser_type)

            # THEN
            ig_browser.get_posts.assert_called_once_with()

        def test_controller_login_called_ok(self, mocks, ig_browser_mock):
            # GIVEN
            ig_browser_type, ig_browser = ig_browser_mock
            controller, login_credentials, _, _ = mocks
            ig_browser.logged_in = False

            # WHEN
            Controller.run(controller, igbrowser_type=ig_browser_type)

            # THEN
            ig_browser.login.assert_called_once_with(login_credentials)
            ig_browser.get_posts.assert_called_once_with()

    class TestGetPosts:
        def test_filter_group_returns_false_ok(self, mocks, ig_browser_mock):
            # GIVEN
            post = Mock()
            ig_browser_type, ig_browser = ig_browser_mock
            controller, _, action, filter_group = mocks
            ig_browser.logged_in = True
            filter_group.return_value = False
            ig_browser.get_posts.return_value = [post]

            # WHEN
            Controller.run(controller, igbrowser_type=ig_browser_type)

            # THEN
            ig_browser.get_posts.assert_called_once_with()
            post.perform_action.assert_not_called()

        def test_filter_group_returns_true_ok(self, mocks, ig_browser_mock):
            # GIVEN
            post = Mock()
            ig_browser_type, ig_browser = ig_browser_mock
            controller, _, action, filter_group = mocks
            ig_browser.logged_in = True
            filter_group.return_value = True
            ig_browser.get_posts.return_value = [post]

            # WHEN
            Controller.run(controller, igbrowser_type=ig_browser_type)

            # THEN
            ig_browser.get_posts.assert_called_once_with()
            post.perform_action.assert_called_once_with(action)


class TestConfigFileParser:
    @pytest.fixture
    def config_mock(self):
        yield io.StringIO(
            """
{
    "username": "xyz",
    "password": "pwd",
    "webdriverPath": "./chromedriver.exe",
    "actions": {
        "post": [
            {
                "actionName": "like",
                "filters": [
                    {
                        "filterName": "ProbabilisticActionFilter",
                        "params": {
                            "probability_success": 0.1
                        }
                    }
                ]
            }
        ]
    }
}
"""
        )

    def test_parse_ok(self, config_mock):
        login_credentials, actions, webdriver_path = config_file_parser(config_mock)
        assert isinstance(actions[Post], list)
        assert isinstance(actions[Post][0], ActionConfig)
        assert isinstance(actions[Post][0].filters, actionfilter.FilterGroup)
        assert webdriver_path == "./chromedriver.exe"
        assert isinstance(login_credentials, LoginCredentials)

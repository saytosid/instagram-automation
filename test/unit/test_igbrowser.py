from igbrowser import IGBrowser, LoginCredentials, Action, Post, rand_sleep, By
import constants


import pytest
from unittest.mock import Mock, MagicMock


def test_login_credentials_are_hidden_while_printing_object():
    lc = LoginCredentials(username="shwiftyrick", password="hunter2")
    assert "shwiftyrick" not in str(lc)
    assert "hunter2" not in str(lc)
    assert "shwiftyrick" not in repr(lc)
    assert "hunter2" not in repr(lc)


def test_rand_sleep():
    def foo():
        ...

    mock_sleep = Mock()
    foo = rand_sleep(foo, _sleep_fn=mock_sleep)

    foo()
    foo()

    assert 2 == mock_sleep.call_count

    ((arg1,), _), ((arg2,), _) = mock_sleep.call_args_list
    assert arg1 != arg2
    assert float is type(arg1)
    assert float is type(arg2)
    assert all(0 < x < 2 for x in (arg1, arg2))


class TestPost:
    @pytest.fixture
    def mock_post(self):
        yield Post(MagicMock(), MagicMock())

    def test_post_perform_action(self, mock_post):
        action1, func1 = object(), MagicMock()
        mock_post._action_dispatcher = {action1: func1}

        mock_post.perform_action(action1, "arg", k="kwarg")

        func1.assert_called_once_with("arg", k="kwarg")

    @pytest.mark.parametrize(
        "name, button_name, aria_label, clicked",
        [
            ("like_normal", "like", "Like", True),
            ("unlike_normal", "unlike", "Unlike", True),
            ("dont_click_if_already_liked", "like", "Unlike", False),
            ("dont_click_if_already_unliked", "unlike", "Like", False),
        ],
    )
    def test_like_unlike_buttons(
        self, name, button_name, aria_label, clicked, mock_post
    ):
        mock_button = MagicMock()
        mock_post.container.find_element.return_value = mock_button
        mock_button.get_attribute.return_value = aria_label
        mock_post._scroll_to_and_click = MagicMock()

        getattr(mock_post, button_name)()

        mock_post.container.find_element.assert_called_once_with(
            By.XPATH, constants.XPATHS["like_unlike_button"]
        )
        mock_button.get_attribute.assert_called_once_with("aria-label")
        if clicked:
            mock_post._scroll_to_and_click.assert_called_once_with(mock_button)
        else:
            assert 0 == mock_post._scroll_to_and_click.call_count

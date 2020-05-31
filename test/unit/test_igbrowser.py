from igbrowser import IGBrowser, LoginCredentials, Action, Post, rand_sleep

from unittest.mock import Mock


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



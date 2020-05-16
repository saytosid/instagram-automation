#!/usr/bin/env python
from session import Session, LoginCredentials
import constants


def sleep(n):
    import time

    time.sleep(n)


class Driver:
    def run(self):
        with Session(LoginCredentials(*constants.USERNAME_PWD)) as browser:
            sleep(3)


if __name__ == "__main__":
    Driver().run()

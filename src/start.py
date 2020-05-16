#!/usr/bin/env python


from selenium.webdriver import Chrome
from selenium.webdriver.firefox.options import Options
# opts = Options()
# opts.set_headless()
# assert opts.headless  # Operating in headless mode
browser = Chrome('./chromedriver.exe')
browser.get('https://duckduckgo.com')

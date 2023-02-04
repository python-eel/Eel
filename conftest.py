import os
from unittest import mock

import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


@pytest.fixture
def driver():
    TEST_BROWSER = os.environ.get("TEST_BROWSER", "chrome").lower()

    if TEST_BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        options.headless = True
        capabilities = DesiredCapabilities.CHROME
        capabilities['goog:loggingPrefs'] = {"browser": "ALL"}

        web_driver = webdriver.Chrome(options=options, desired_capabilities=capabilities, service_log_path=os.path.devnull)

        # If errors with chromium version, add path to particular version here
        # web_driver = webdriver.Chrome(executable_path=r"C:\Users\Turtor\Desktop\chromedriver.exe", options=options, desired_capabilities=capabilities, service_log_path=os.path.devnull)



    else:
        raise ValueError(f"Unsupported browser for testing: {TEST_BROWSER}")

    with mock.patch("eel.browsers.open"):
        try:
            yield web_driver
            web_driver.quit()
        except Exception:
            pass



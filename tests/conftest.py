import os
import platform
from unittest import mock

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    TEST_BROWSER = os.environ.get("TEST_BROWSER", "chrome").lower()

    if TEST_BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

        if platform.system() == "Windows":
            options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )

    # Firefox doesn't currently supported pulling JavaScript console logs, which we currently scan to affirm that
    # JS/Python can communicate in some places. So for now, we can't really use firefox/geckodriver during testing.
    # This may be added in the future: https://github.com/mozilla/geckodriver/issues/284

    # elif TEST_BROWSER == "firefox":
    #     options = webdriver.FirefoxOptions()
    #     options.headless = True
    #     capabilities = DesiredCapabilities.FIREFOX
    #     capabilities['loggingPrefs'] = {"browser": "ALL"}
    #
    #     driver = webdriver.Firefox(options=options, capabilities=capabilities, service_log_path=os.path.devnull)

    else:
        raise ValueError(f"Unsupported browser for testing: {TEST_BROWSER}")

    with mock.patch("eel.browsers.open"):
        yield driver

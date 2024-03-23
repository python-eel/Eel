import os
import platform
from unittest import mock

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def detect_chrome_path() -> str:
    locations_windows = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    locations_mac = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    ]
    locations_linux = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome-beta",
        "/usr/bin/google-chrome-unstable",
    ]
    
    if platform.system() == "Linux":
        for location in locations_linux:
            if os.path.exists(location):
                return location
    elif platform.system() == "Darwin":
        for location in locations_mac:
            if os.path.exists(location):
                return location
    elif platform.system() == "Windows":
        for location in locations_windows:
            if os.path.exists(location):
                return location

# @pytest.fixture
# def driver():
#     TEST_BROWSER = os.environ.get("TEST_BROWSER", "chrome").lower()

#     if TEST_BROWSER == "chrome":
#         chrome_options = webdriver.ChromeOptions()
#         # chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--enable-logging")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.binary_location = detect_chrome_path()
        
#         # chrome_service = ChromeService(ChromeDriverManager().install())
#         # driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
#         driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#         driver.set_window_size(1920, 1080)
#         driver.implicitly_wait(10)
#         driver.set_page_load_timeout(10)
#         print(driver.current_url)
#         # driver = webdriver.Chrome(
#         #     ChromeDriverManager().install(),
#         #     options=chrome_options,
#         #     desired_capabilities=capabilities,
#         #     service_log_path=os.path.devnull,
#         # )

#         # Firefox doesn't currently supported pulling JavaScript console logs, which we currently scan to affirm that
#         # JS/Python can communicate in some places. So for now, we can't really use firefox/geckodriver during testing.
#         # This may be added in the future: https://github.com/mozilla/geckodriver/issues/284

#     # elif TEST_BROWSER == "firefox":
#     #     options = webdriver.FirefoxOptions()
#     #     options.headless = True
#     #     capabilities = DesiredCapabilities.FIREFOX
#     #     capabilities['loggingPrefs'] = {"browser": "ALL"}
#     #
#     #     driver = webdriver.Firefox(options=options, capabilities=capabilities, service_log_path=os.path.devnull)

#     else:
#         raise ValueError(f"Unsupported browser for testing: {TEST_BROWSER}")

#     with mock.patch("paling.browsers.open"):
#         yield driver

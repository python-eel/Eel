import os
import time
from tempfile import TemporaryDirectory, NamedTemporaryFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.utils import get_eel_server, get_console_logs


def test_01_hello_world(driver):
    with get_eel_server('examples/01 - hello_world/hello.py', 'hello.html') as eel_url:
        driver.get(eel_url)
        assert driver.title == "Hello, World!"

        console_logs = get_console_logs(driver, minimum_logs=2)
        assert "Hello from Javascript World!" in console_logs[0]['message']
        assert "Hello from Python World!" in console_logs[1]['message']


def test_02_callbacks(driver):
    with get_eel_server('examples/02 - callbacks/callbacks.py', 'callbacks.html') as eel_url:
        driver.get(eel_url)
        assert driver.title == "Callbacks Demo"

        console_logs = get_console_logs(driver, minimum_logs=1)
        assert "Got this from Python:" in console_logs[0]['message']
        assert "callbacks.html" in console_logs[0]['message']


def test_03_callbacks(driver):
    with get_eel_server('examples/03 - sync_callbacks/sync_callbacks.py', 'sync_callbacks.html') as eel_url:
        driver.get(eel_url)
        assert driver.title == "Synchronous callbacks"

        console_logs = get_console_logs(driver, minimum_logs=1)
        assert "Got this from Python:" in console_logs[0]['message']
        assert "callbacks.html" in console_logs[0]['message']


def test_04_file_access(driver: webdriver.Remote):
    with get_eel_server('examples/04 - file_access/file_access.py', 'file_access.html') as eel_url:
        driver.get(eel_url)
        assert driver.title == "Eel Demo"

        with TemporaryDirectory() as temp_dir, NamedTemporaryFile(dir=temp_dir) as temp_file:
            driver.find_element(value='input-box').clear()
            driver.find_element(value='input-box').send_keys(temp_dir)
            time.sleep(0.5)
            driver.find_element(By.CSS_SELECTOR, 'button').click()

            assert driver.find_element(value='file-name').text == os.path.basename(temp_file.name)


def test_06_jinja_templates(driver: webdriver.Remote):
    with get_eel_server('examples/06 - jinja_templates/hello.py', 'templates/hello.html') as eel_url:
        driver.get(eel_url)
        assert driver.title == "Hello, World!"

        driver.find_element(By.CSS_SELECTOR, 'a').click()
        WebDriverWait(driver, 2.0).until(expected_conditions.presence_of_element_located((By.XPATH, '//h1[text()="This is page 2"]')))


def test_10_custom_app(driver: webdriver.Remote):
    # test default eel routes are working
    with get_eel_server('examples/10 - custom_app_routes/custom_app.py', 'index.html') as eel_url:
        driver.get(eel_url)
        # we really need to test if the page 404s, but selenium has no support for status codes
        # so we just test if we can get our page title
        assert driver.title == 'Hello, World!'

    # test custom routes are working
    with get_eel_server('examples/10 - custom_app_routes/custom_app.py', 'custom') as eel_url:
        driver.get(eel_url)
        assert 'Hello, World!' in driver.page_source

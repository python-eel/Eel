import os
import re
import shutil
import tempfile
import time
from tempfile import TemporaryDirectory, NamedTemporaryFile

import pytest
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
            driver.find_element_by_id('input-box').clear()
            driver.find_element_by_id('input-box').send_keys(temp_dir)

            fname = driver.find_element_by_id('file-name').text
            while fname != os.path.basename(temp_file.name):
                driver.find_element_by_css_selector('button').click()
                time.sleep(0.05)
                fname = driver.find_element_by_id('file-name').text


def test_06_jinja_templates(driver: webdriver.Remote):
    with get_eel_server('examples/06 - jinja_templates/hello.py', 'templates/hello.html') as eel_url:
        driver.get(eel_url)
        assert driver.title == "Hello, World!"

        driver.find_element_by_css_selector('a').click()
        WebDriverWait(driver, 2.0).until(expected_conditions.presence_of_element_located((By.XPATH, '//h1[text()="This is page 2"]')))


@pytest.mark.timeout(30)
def test_10_reload_file_changes(driver: webdriver.Remote):
    with tempfile.TemporaryDirectory() as tmp_root:
        tmp_dir = shutil.copytree(
            os.path.join("examples", "10 - reload_code"), os.path.join(tmp_root, "test_10")
        )

        with get_eel_server(
            os.path.join(tmp_dir, "reloader.py"), "reloader.html"
        ) as eel_url:
            driver.get(eel_url)
            assert driver.title == "Reloader Demo"

            msg = driver.find_element_by_id("updating-message").text
            assert msg == "---"

            while msg != (
                "Change this message in `reloader.py` and see it available in the browser after a few seconds/clicks."
            ):
                time.sleep(0.05)
                driver.find_element_by_xpath("//button").click()
                msg = driver.find_element_by_id("updating-message").text

            # Update the test code file and change the message.
            reloader_code = open(os.path.join(tmp_dir, "reloader.py")).read()
            reloader_code = re.sub(
                '^ {4}return ".*"$', '    return "New message."', reloader_code, flags=re.MULTILINE
            )

            with open(os.path.join(tmp_dir, "reloader.py"), "w") as f:
                f.write(reloader_code)

            # Nudge the dev server to give it a chance to reload
            driver.get(eel_url)

            while msg != "New message.":
                time.sleep(0.05)
                driver.find_element_by_xpath("//button").click()
                msg = driver.find_element_by_id("updating-message").text

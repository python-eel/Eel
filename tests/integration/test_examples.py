import os
import time
from tempfile import TemporaryDirectory, NamedTemporaryFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.utils import get_paling_server, get_console_logs

def test_00_index(driver=None):
    print("test_00_index")

# def test_01_hello_world(driver: webdriver.Remote):
#     print("test_01_hello_world")
#     with get_paling_server('examples/01 - hello_world/hello.py', 'hello.html') as paling_url:
#         driver.get(paling_url)
#         assert driver.title == "Hello, World!"

#         console_logs = get_console_logs(driver, minimum_logs=2)
#         assert "Hello from Javascript World!" in console_logs[0]['message']
#         assert "Hello from Python World!" in console_logs[1]['message']


# def test_02_callbacks(driver: webdriver.Remote):
#     print("test_02_callbacks")
#     with get_paling_server('examples/02 - callbacks/callbacks.py', 'callbacks.html') as paling_url:
#         driver.get(paling_url)
#         assert driver.title == "Callbacks Demo"

#         console_logs = get_console_logs(driver, minimum_logs=1)
#         assert "Got this from Python:" in console_logs[0]['message']
#         assert "callbacks.html" in console_logs[0]['message']


# def test_03_callbacks(driver: webdriver.Remote):
#     print("test_03_callbacks")
#     with get_paling_server('examples/03 - sync_callbacks/sync_callbacks.py', 'sync_callbacks.html') as paling_url:
#         driver.get(paling_url)
#         assert driver.title == "Synchronous callbacks"

#         console_logs = get_console_logs(driver, minimum_logs=1)
#         assert "Got this from Python:" in console_logs[0]['message']
#         assert "callbacks.html" in console_logs[0]['message']


# def test_04_file_access(driver: webdriver.Remote):
#     print("test_04_file_access")
#     with get_paling_server('examples/04 - file_access/file_access.py', 'file_access.html') as paling_url:
#         driver.get(paling_url)
#         assert driver.title == "Paling Demo"

#         with TemporaryDirectory() as temp_dir, NamedTemporaryFile(dir=temp_dir) as temp_file:
#             driver.find_element_by_id('input-box').clear()
#             driver.find_element_by_id('input-box').send_keys(temp_dir)
#             time.sleep(0.5)
#             driver.find_element_by_css_selector('button').click()

#             assert driver.find_element_by_id('file-name').text == os.path.basename(temp_file.name)


# def test_06_jinja_templates(driver: webdriver.Remote):
#     print("test_06_jinja_templates")
#     with get_paling_server('examples/06 - jinja_templates/hello.py', 'templates/hello.html') as paling_url:
#         driver.get(paling_url)
#         assert driver.title == "Hello, World!"

#         driver.find_element_by_css_selector('a').click()
#         WebDriverWait(driver, 2.0).until(expected_conditions.presence_of_element_located((By.XPATH, '//h1[text()="This is page 2"]')))


# def test_10_custom_app(driver: webdriver.Remote):
#     print("test_10_custom_app")
#     # test default paling routes are working
#     with get_paling_server('examples/10 - custom_app_routes/custom_app.py', 'index.html') as paling_url:
#         driver.get(paling_url)
#         # we really need to test if the page 404s, but selenium has no support for status codes
#         # so we just test if we can get our page title
#         assert driver.title == 'Hello, World!'

#     # test custom routes are working
#     with get_paling_server('examples/10 - custom_app_routes/custom_app.py', 'custom') as paling_url:
#         driver.get(paling_url)
#         assert 'Hello, World!' in driver.page_source

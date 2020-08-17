import contextlib
import os
import subprocess
import tempfile
import time
from pathlib import Path

import psutil

# Path to the test data folder.
TEST_DATA_DIR = Path(__file__).parent / 'data'


def get_process_listening_port(proc):
    psutil_proc = psutil.Process(proc.pid)
    while not any(conn.status == 'LISTEN' for conn in psutil_proc.connections()):
        time.sleep(0.01)

    conn = next(filter(lambda conn: conn.status == 'LISTEN', psutil_proc.connections()))
    return conn.laddr.port


@contextlib.contextmanager
def get_eel_server(example_py, start_html):
    """Run an Eel example with the mode/port overridden so that no browser is launched and a random port is assigned"""
    test = None

    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=os.path.dirname(example_py), delete=False) as test:
            # We want to run the examples unmodified to keep the test as realistic as possible, but all of the examples
            # want to launch browsers, which won't be supported in CI. The below script will configure eel to open on
            # a random port and not open a browser, before importing the Python example file - which will then
            # do the rest of the set up and start the eel server. This is definitely hacky, and means we can't
            # test mode/port settings for examples ... but this is OK for now.
            test.write(f"""
import eel

eel._start_args['mode'] = None
eel._start_args['port'] = 0

import {os.path.splitext(os.path.basename(example_py))[0]}
""")

        proc = subprocess.Popen(['python', test.name], cwd=os.path.dirname(example_py))
        eel_port = get_process_listening_port(proc)

        yield f"http://localhost:{eel_port}/{start_html}"

        proc.terminate()

    finally:
        if test:
            try:
                os.unlink(test.name)
            except FileNotFoundError:
                pass


def get_console_logs(driver, minimum_logs=0):
    console_logs = driver.get_log('browser')

    while len(console_logs) < minimum_logs:
        console_logs += driver.get_log('browser')
        time.sleep(0.1)

    return console_logs

import contextlib
import os
import random
import socket
import string
import subprocess
import tempfile
import time

import psutil


def is_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(("localhost", port)) == 0


@contextlib.contextmanager
def get_eel_server(example_py, start_html):
    """Run an Eel example with the mode/port overridden so that no browser is launched and a random port is assigned"""
    test = None

    # Find a port for Eel to run on
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        eel_port = sock.getsockname()[1]

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
eel._start_args['port'] = {eel_port}

import {os.path.splitext(os.path.basename(example_py))[0]}
""")

        proc = subprocess.Popen(['python', test.name], cwd=os.path.dirname(example_py), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        while not is_port_open(eel_port):
            time.sleep(0.01)

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

import eel
import pytest
from tests.utils import TEST_DATA_DIR

# Directory for testing eel.__init__
INIT_DIR = TEST_DATA_DIR / 'init_test'


@pytest.mark.parametrize('js_code, expected_matches', [
    ('eel.expose(w,"say_hello_js")', ['say_hello_js']),
    ('eel.expose(function(e){console.log(e)},"show_log_alt")', ['show_log_alt']),
    (' \t\nwindow.eel.expose((function show_log(e) {console.log(e)}), "show_log")\n', ['show_log']),
    ((INIT_DIR / 'minified.js').read_text(), ['say_hello_js', 'show_log_alt', 'show_log']),
    ((INIT_DIR / 'sample.html').read_text(), ['say_hello_js']),
    ((INIT_DIR / 'App.tsx').read_text(), ['say_hello_js', 'show_log']),
    ((INIT_DIR / 'hello.html').read_text(), ['say_hello_js', 'js_random']),
])
def test_exposed_js_functions(js_code, expected_matches):
    """Test the PyParsing PEG against several specific test cases."""
    matches = eel.EXPOSED_JS_FUNCTIONS.parseString(js_code).asList()
    assert matches == expected_matches, f'Expected {expected_matches} (found: {matches}) in: {js_code}'

@pytest.mark.parametrize('kwargs, exposed_functions', [
    ({"path": INIT_DIR}, ["show_log", "js_random", "ignore_test", "show_log_alt", "say_hello_js"]),
    ({"path": INIT_DIR, "exclude_file_prefixes": ["ignore"]}, ["show_log", "js_random", "show_log_alt", "say_hello_js"]),
    ({"path": INIT_DIR, "use_only_files": ["hello.html"]}, ["js_random", "say_hello_js"]),
])
def test_init_file_excluding(kwargs, exposed_functions):
    """Test eel.init() against a test directory and ensure that all JS functions are in the global _js_functions."""
    eel.init(**kwargs)
    result = eel._js_functions
    assert set(result) == set(exposed_functions), f"Expected {exposed_functions} (found: {result}) in {INIT_DIR}"

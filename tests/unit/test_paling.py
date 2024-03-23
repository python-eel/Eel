import paling
import pytest
from tests.utils import TEST_DATA_DIR

# Directory for testing paling.__init__
INIT_DIR = TEST_DATA_DIR / 'init_test'


# @pytest.mark.parametrize('js_code, expected_matches', [
#     ('paling.expose(w,"say_hello_js")', ['say_hello_js']),
#     ('paling.expose(function(e){console.log(e)},"show_log_alt")', ['show_log_alt']),
#     (' \t\nwindow.paling.expose((function show_log(e) {console.log(e)}), "show_log")\n', ['show_log']),
#     ((INIT_DIR / 'minified.js').read_text(), ['say_hello_js', 'show_log_alt', 'show_log']),
#     ((INIT_DIR / 'sample.html').read_text(), ['say_hello_js']),
#     ((INIT_DIR / 'App.tsx').read_text(), ['say_hello_js', 'show_log']),
#     ((INIT_DIR / 'hello.html').read_text(), ['say_hello_js', 'js_random']),
# ])
# def test_exposed_js_functions(js_code, expected_matches):
#     """Test the PyParsing PEG against several specific test cases."""
#     matches = paling.EXPOSED_JS_FUNCTIONS.parseString(js_code).asList()
#     assert matches == expected_matches, f'Expected {expected_matches} (found: {matches}) in: {js_code}'


# def test_init():
#     """Test paling.init() against a test directory and ensure that all JS functions are in the global _js_functions."""
#     paling.init(path=INIT_DIR)
#     result = paling._js_functions.sort()
#     functions = ['show_log', 'js_random', 'show_log_alt', 'say_hello_js'].sort()
#     assert result == functions, f'Expected {functions} (found: {result}) in {INIT_DIR}'

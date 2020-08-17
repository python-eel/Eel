# Eel Developers

## Setting up a development environment

In order to start developing with Eel you'll need to checkout the code, set up a development and testing environment, and check that everything is in order.

Clone the repository:
```bash
git clone git@github.com:samuelhwilliams/Eel.git
```

Create a dev virtual environment. Your process for doing this may vary, but might look something like this (assuming you have `venv` in a global `.gitignore` file):

```bash
python3 -m venv venv
source venv/bin/activate
```

We support Python 3.6+ so developers should ideally run their tests against the latest minor version of each major version we support from there. Tox is configured to run tests against each major version we support. In order to run tox fully, you will need to install multiple versions of Python. See the pinned minor versions in `.python-version`.

## Running tests

To test Eel against a specific version of Python you have installed, e.g. Python 3.6 in this case, run:

```bash
tox -e py36
```

To test Eel against all supported versions, run the following:

```bash
tox
```

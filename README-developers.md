# Eel Developers

## Setting up your environment

In order to start developing with Eel you'll need to checkout the code, set up a development and testing environment, and check that everything is in order.

### Clone the repository
```bash
git clone git@github.com:python-eel/Eel.git
```

### (Recommended) Create a virtual environment
It's recommended that you use virtual environments for this project. Your process for setting up a virutal environment will vary depending on OS and tool of choice, but might look something like this:

```bash
python3 -m venv venv
source venv/bin/activate
```

**Note**: `venv` is listed in the `.gitignore` file so it's the recommended virtual environment name
    

### Install project requirements

```bash
pip3 install -r requirements.txt        # eel's 'prod' requirements
pip3 install -r requirements-test.txt   # pytest and selenium
pip3 install -r requirements-meta.txt   # tox 
```

### (Recommended) Run Automated Tests
Tox is configured to run tests against each major version we support (3.7+). In order to run Tox as configured, you will need to install multiple versions of Python. See the pinned minor versions in `.python-version` for recommendations.

#### Tox Setup
Our Tox configuration requires [Chrome](https://www.google.com/chrome) and [ChromeDriver](https://chromedriver.chromium.org/home). See each of those respective project pages for more information on setting each up.

**Note**: Pay attention to the version of Chrome that is installed on your OS because you need to select the compatible ChromeDriver version.

#### Running Tests

To test Eel against a specific version of Python you have installed, e.g. Python 3.7 in this case, run:

```bash
tox -e py36
```

To test Eel against all supported versions, run the following:

```bash
tox
```

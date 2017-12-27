# Eel
Eel is a little Python library for making simple Electron-like offline HTML/JS GUI apps, with full access to Python capabilities and libraries. It lets you annotate functions in Python so that they can be called from Javascript, and vice versa.

### Intro

There are several options for making GUI apps in Python, but if you want to use HTML/JS you generally have to write a lot of boilerplate code to communicate from the Client (Javascript) side to the Server (Python) side.

There is currently (to my knowledge) no Python equivalent of Electron - something that let's you write a standalone application in Python with an HTML frontend. Eel is not a fully-fledged as Electron - it is probably not suitable for making full blown applications like Atom - but it is very suitable for making the GUI equivalent of little utility scrips you use yourself.

### Install

Install from pypi with `pip`:

    pip install eel

### Usage

#### Structure

An application that uses Eel will be split into a frontend consisting of various web-technology files (.html, .js, .css) and a backend consisting of various Python scripts.

All the frontend files should be put in a single directory (they can be further divided into folders inside this if necessary).

#### Starting the app

Suppose you put all the frontend files in a directory called `web`, including your start page `index.html`, then app is started like this;

```python
import eel
eel.init('web')
eel.start('index.html')
```

This will start a webserver on the default settings (http://localhost:8000) and open a browser to http://localhost:8000/index.html.

If Chrome is installed then by default it will open in Chrome in App Mode (with the `--app` cmdline flag), regardless of what your default browser is. It is possible to override this behaviour.

#### Exposing functions

In addition to the files in the frontend folder, a Javascript library will be served at `/eel.js`. You should include this in any pages:

```html
<script type="text/javascript" src="/eel.js"></script>
```
Including this library creates an `eel` object which can be used to communicate with the Python side.

Any functions in the Python code which are decorated with `@eel.expose` like this...
```python
@eel.expose
def my_python_function(a, b):
    print(a, b, a + b)
```
...will appear as methods on the `eel` object on the Javascript side, like this...
```html
<script type="text/javascript">
  console.log('Calling Python...');
  eel.my_python_function(1, 2);
</script>
```

Similarly, any Javascript functions which are exposed like this...
```html
<script type="text/javascript">
  eel.expose(my_js_function);
  function my_js_function(a, b, c, d) {
    if(a < b){
     console.log(c * d);
    }
  }
</script>
```
can be called from the Python side like this...
```python
print('Calling Javascript')
eel.my_js_function(1, 2, 3, 4);
```

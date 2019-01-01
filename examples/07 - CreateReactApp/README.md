# README

Eello World example Create-React-App (CRA) with Eel. This particular project was bootstrapped with `npx create-react-app 07_CreateReactApp --typescript` (Typescript enabled), but the below modifications can be implemented in any CRA configuration or CRA version.

If you run into any issues with this example, open a [new issue](https://github.com/ChrisKnott/Eel/issues/new) and tag @KyleKing

## Quick Start

1. In the app's directory, run `npm install` and `pip install bottle bottle-websocket future whichcraft pyinstaller`
2. Build the application with `npm run build`
3. Run the built version with `python eel_CRA.py`. A Chrome window should open running the code from `build/`
4. Build a binary distribution with PyInstaller using `python -m eel eel_CRA.py build --onefile` (See more detailed instructions at bottom of [the main README](https://github.com/ChrisKnott/Eel))
5. For development, open two prompts. In one, run  `python eel_CRA.py true` and the other, `npm start`. A browser window should open in your default web browser at: [http://localhost:3000/](http://localhost:3000/). As you make changes to the JavaScript in `src/` the browser will reload. Any changes to `eel_CRA.py` will require a restart to take effect. You may need to refresh the browser window if it gets out of sync with eel.

![Demo.png](Demo.png)

## About

These are the changes needed to convert the basic CRA application for Eel support.

### Use `window.eel.expose(func, 'func')` with `npm run build`

> TLDR: CRA's default code mangling in `npm run build` will rename variables and functions. To handle these changes, convert all `eel.expose(funcName)` to `window.eel(funcName, 'funcName')`. This workaround guarantees that 'funcName' will be available to call from Python

When you run `npm run build`, CRA generates a mangled and minified JavaScript file. The mangling will change `eel.expose(funcName)` to something like `D.expose(J)`. The modified code won't be recognized by the Eel static JS-code analyzer, which uses a regular expression to look for `eel.expose(*)` and the function name expected in python, `funcName`, is now mangled as `J`.

The easy workaround is just to refactor `eel.expose(funcName)` to `window.eel(funcName, 'func_name')` where `window.eel` prevents `eel` from being mangled. Then `eel.func_name()` can be called from Python

### src/App.tsx

Modified to demonstrate exposing a function from JavaScript and how to use callbacks from Python to update React GUI.

### eel_CRA.py

Basic eel file that exposes two Python functions to JavaScript. If a second argument (i.e. `true`) is provided, the app uses a development mode for a server already alive on port 3000; otherwise, the script will load `index.html` from the build/ directory, which is what you want for building from a binary.

### public/index.html

Added location of `eel.js` file based on options set in eel_CRA.py.

```html
<!-- Load eel.js from the port specified in the eel.start options -->
<script type="text/javascript" src="http://localhost:8080/eel.js"></script>
```

### src/react-app-env.d.ts

This file declares window.eel as a valid type for tslint. Note: capitalization of `window`


### src/App.css

Added some basic button styling :)

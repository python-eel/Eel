# Change log

### v0.14.0
* Change JS function name parsing to use PyParsing rather than regex, courtesy @KyleKing.

### v0.13.2
* Add `default_path` start arg to define a default file to retrieve when hitting the root URL.

### v0.13.1
* Shut down the Eel server less aggressively when websockets get closed (#337)

## v0.13.0
* Drop support for Python versions below 3.6
* Add `jinja2` as an extra for pip installation, e.g. `pip install eel[jinja2]`.
* Bump dependencies in examples to dismiss github security notices. We probably want to set up a policy to ignore example dependencies as they shouldn't be considered a source of vulnerabilities.
* Disable edge on non-Windows platforms until we implement proper support.

### v0.12.4
* Return greenlet task from `spawn()` ([#300](https://github.com/samuelhwilliams/Eel/pull/300))
* Set JS mimetype to reduce errors on Windows platform ([#289](https://github.com/samuelhwilliams/Eel/pull/289))

### v0.12.3
* Search for Chromium on macOS.

### v0.12.2
* Fix a bug that prevents using middleware via a custom Bottle.

### v0.12.1
* Check that Chrome path is a file that exists on Windows before blindly returning it.

## v0.12.0
* Allow users to override the amount of time Python will wait for Javascript functions running via Eel to run before bailing and returning None.

### v0.11.1
* Fix the implementation of #203, allowing users to pass their own bottle instances into Eel.

## v0.11.0
* Added support for `app` parameter to `eel.start`, which will override the bottle app instance used to run eel. This
allows developers to apply any middleware they wish to before handing over to eel.
* Disable page caching by default via new `disable_cache` parameter to `eel.start`.
* Add support for listening on all network interfaces via new `all_interfaces` parameter to `eel.start`.
* Support for Microsoft Edge

### v0.10.4
* Fix PyPi project description.

### v0.10.3
* Fix a bug that prevented using Eel without Jinja templating.

### v0.10.2
* Only render templates from within the declared jinja template directory.

### v0.10.1
* Avoid name collisions when using Electron, so jQuery etc work normally

## v0.10.0
* Corrective version bump after new feature included in 0.9.13
* Fix a bug with example 06 for Jinja templating; the `templates` kwarg to `eel.start` takes a filepath, not a bool.

### v0.9.13
* Add support for Jinja templating.

### Earlier
* No changelog notes for earlier versions.

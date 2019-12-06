# Change log

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

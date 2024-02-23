# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Based on https://github.com/niwinz/django-jinja/blob/master/django_jinja/library.py

_registry = {
    "extensions": set(),
    "filter_functions": {},
    "global_functions": {},
}


def update_jinja2_env(env):
    for extension in _registry["extensions"]:
        env.add_extension(extension)
    env.filters.update(_registry["filter_functions"])
    env.globals.update(_registry["global_functions"])
    return env


def _attach_function_to_registry(attr, func, name=None):
    if name is None:
        name = func.__name__

    global _registry
    _registry[attr][name] = func
    return func


def _register_function(attr, name=None, fn=None):
    if name is None and fn is None:

        def dec(func):
            return _attach_function_to_registry(attr, func)

        return dec

    elif name is not None and fn is None:
        if callable(name):
            return _attach_function_to_registry(attr, name)
        else:

            def dec(func):
                return _register_function(attr, name, func)

            return dec

    elif name is not None and fn is not None:
        return _attach_function_to_registry(attr, fn, name)

    raise RuntimeError("Invalid parameters")


def extension(extension):
    global _registry
    _registry["extensions"].add(extension)
    return extension


def filter(*args, **kwargs):
    return _register_function("filter_functions", *args, **kwargs)


def global_function(*args, **kwargs):
    return _register_function("global_functions", *args, **kwargs)

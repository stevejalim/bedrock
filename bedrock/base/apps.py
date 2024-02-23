# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "bedrock.base"
    label = "base"

    def ready(self):
        # Import the templatetags so that they are registered with bedrock.jinja2

        # Note: lib/ is not a regular Django app, so doesn't have an AppConfig.
        # We'll deal with that by importing here
        from lib.l10n_utils.templatetags import fluent as fluent, helpers as l10n_helpers  # noqa: F401

        from .templatetags import helpers  # noqa: F401

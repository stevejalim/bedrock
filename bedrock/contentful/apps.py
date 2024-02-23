# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.apps import AppConfig


class ContentfulConfig(AppConfig):
    name = "bedrock.contentful"
    label = "contentful"

    def ready(self):
        # Import the templatetags so that they are registered with bedrock.jinja2
        from .templatetags import helpers  # noqa: F401

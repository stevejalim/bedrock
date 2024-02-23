# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import bleach
from markupsafe import Markup

from bedrock.jinja2 import library

# based on bleach.sanitizer.ALLOWED_TAGS
ALLOWED_TAGS = {
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "button",
    "code",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "small",
    "span",
    "strike",
    "strong",
    "ul",
}
ALLOWED_ATTRS = [
    "alt",
    "class",
    "href",
    "id",
    "src",
    "srcset",
    "rel",
    "title",
]


def _allowed_attrs(tag, name, value):
    if name in ALLOWED_ATTRS:
        return True

    if name.startswith("data-"):
        return True

    return False


@library.filter
def external_html(content):
    """Clean and mark "safe" HTML content from external data"""
    return Markup(bleach.clean(content, tags=ALLOWED_TAGS, attributes=_allowed_attrs))

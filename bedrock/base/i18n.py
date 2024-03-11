# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import django.urls
from django.conf import settings
from django.utils.translation.trans_real import parse_accept_lang_header

from lib.l10n_utils import translation


class LocalePrefixPattern(django.urls.LocalePrefixPattern):
    """
    A sub-class of Django's "LocalePrefixPattern" that simply normalizes the language
    prefix for Bedrock (e.g., upper-case country codes).

    This is an essential piece, since it controls the resolution of the
    language-code prefix of incoming URLs as well as the language code prefix
    of the URLs generated by Django's "reverse".
    """

    @property
    def language_prefix(self):
        language_code = normalize_language(translation.get_language()) or settings.LANGUAGE_CODE
        if language_code == settings.LANGUAGE_CODE and not self.prefix_default_language:
            return ""
        return f"{language_code}/"


def path_needs_lang_code(path):
    """Convenient way to spot if a path needs a prefix or not"""
    if path in settings.SUPPORTED_LOCALE_IGNORE:
        return False

    if path.lstrip("/").split("/")[0] in settings.SUPPORTED_NONLOCALES:
        return False

    return True


def bedrock_i18n_patterns(*urls, prefix_default_language=True):
    """
    Similar to Django's i18n_patterns but uses our "LocalePrefixPattern", defined above
    """
    if not settings.USE_I18N:
        return list(urls)
    return [
        django.urls.URLResolver(
            LocalePrefixPattern(prefix_default_language=prefix_default_language),
            list(urls),
        )
    ]


def normalize_language(language):
    """
    Given a language code, returns the language code supported by Bedrock
    in the proper case, for example "eN-us" --> "en-US" - or None if
    Bedrock doesn't support the language code.

    We also convert it to a specified fallback language if the actual
    presented code is not available _and_ we have a fallback specced in
    settings.

    """

    if not language:
        return None

    if settings.IS_POCKET_MODE:
        lang_code = language.lower()
    else:
        lang_code = language

    if lang_code in settings.LANGUAGE_URL_MAP_WITH_FALLBACKS:
        return settings.LANGUAGE_URL_MAP_WITH_FALLBACKS[lang_code]

    # Reformat the lang code to be mixed-case, as we expect
    # them to be for our lookup
    lang, _partition, territory = language.partition("-")
    lang = lang.lower()  # this part is _always_ lowercase

    if territory:
        # Support patterns like ja-JP-mac
        if "-" in territory:
            _territory, _partition, rest = territory.partition("-")
            territory = f"{_territory.upper()}-{rest}"
        else:
            territory = territory.upper()

        lang_code = f"{lang}-{territory}"
    else:
        lang_code = lang

    try:
        return settings.LANGUAGE_URL_MAP_WITH_FALLBACKS[lang_code]
    except KeyError:
        pre = lang_code.split("-")[0]
        return settings.LANGUAGE_URL_MAP_WITH_FALLBACKS.get(pre)


def split_path_and_polish_lang(path_):
    """
    Split the requested path into (lang, path) and
    switches to a supported lang if available

    locale will be empty if it isn't found.

    Returns:
        - lang code (str, may be empty)
        - remaining URL path (str)
        - whether or not the lang code changed (bool)

    """
    path = path_.lstrip("/")

    # Use partition instead of split since it always returns 3 parts
    extracted_lang, _, rest = path.partition("/")

    supported_lang = normalize_language(extracted_lang)
    different = extracted_lang != supported_lang

    if extracted_lang and supported_lang:
        return supported_lang, rest, different
    else:
        return "", path, False


def get_language(request):
    """
    Return a locale code we support on the site using the
    user's Accept-Language header to determine which is best. This
    mostly follows the RFCs but read bug 439568 for details.
    """
    accept_lang = request.headers.get("Accept-Language")
    if accept_lang:
        best = get_best_language(accept_lang)
        if best:
            return best

    return settings.LANGUAGE_CODE


def get_best_language(accept_lang):
    """Given an Accept-Language header, return the best-matching language."""
    ranked = parse_accept_lang_header(accept_lang)
    for lang, _ in ranked:
        supported = normalize_language(lang)
        if supported:
            return supported

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.download import DownloadPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_download_button_displayed(base_url, selenium):
    page = DownloadPage(selenium, base_url).open()
    assert page.is_download_button_displayed

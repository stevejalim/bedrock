# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class Windows64BitPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/browsers/windows-64-bit/"

    _windows_64bit_hero_download_button_locator = (By.ID, "win64-hero-download")
    _windows_64bit_footer_download_button_locator = (By.ID, "win64-bottom-download")

    @property
    def is_windows_64_bit_hero_download_button_displayed(self):
        return self.is_element_displayed(*self._windows_64bit_hero_download_button_locator)

    @property
    def is_windows_64_bit_footer_download_button_displayed(self):
        return self.is_element_displayed(*self._windows_64bit_footer_download_button_locator)

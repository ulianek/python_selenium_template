import pytest
from selenium import webdriver

from Data.websites import urls
from Modules.Pages.base_page import BasePage
from Modules.lalalal import BigClass
from Tests.config import Config


class TestAppearance(object):
    @pytest.mark.parametrize("url", urls, scope="class")
    def test_appearance(self, driver: webdriver.Chrome, url, screenshot_folder):
        BigClass().add()
        driver.get(url)
        base_page = BasePage(driver)
        base_page.get_screenshots_of_entire_page(Config.SCREENSHOTS_PATH, ("heh") + str(urls.index(url)), merge=True)

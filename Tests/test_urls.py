import datetime
import os
import pytest
import pytz

from Data.websites import urls
from Modules.Helpers.gmail_service import get_link_from_mail
from Modules.Helpers.webdriver_extension import WebDriver
from Modules.Helpers.webdriver_m_extension import WebDriverMobile
from Modules.Pages.base_page import BasePage
from Modules.config import Config


@pytest.fixture(scope="class")
def clear_screenshots():
    @pytest.fixture(scope="module")
    def driver_ext():
        folder = Config.SCREENSHOTS_PATH
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


class TestAppearance(object):
    @pytest.mark.parametrize("url", urls, scope="class")
    def test_appearance(self, driver: WebDriver, url):
        driver.get(url)
        base_page = BasePage()
        base_page.screenshot_hp.get_screenshots_of_entire_page()
        remove = driver.find_element_by_xpath("//div[@class='main-bar solid shadowed']")
        driver.get_screenshots_of_entire_page(Config.SCREENSHOTS_PATH, ("heh") +str(urls.index(url)),merge=False, remove_element=remove)



from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Modules.Helpers.webdriver_extension import WebDriver
from Modules.config import Config


class BasePage(object):

    def __init__(self, driver: WebDriver):
        self.basic_url = self.url = Config.BASE_URL
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)
        return self

    def compare_url(self):
        if self.driver.current_url == self.url:
            return True
        else:
            return False

    def save_screenshot(self, file_name):
        entire_page_height = self.driver.execute_script("return document.body.scrollHeight")
        windows_height = self.driver.get_window_size()['height']

        self.driverdriver.get_screenshot_as_file(("Screenshots/" + file_name + ".png"))

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def click_on(self, locator):
        self.driver.wait_for_element_and_click(locator)

    def type(self, locator, text, clear=True):
        self.driver.wait_for_element_and_send_text(locator, text, clear=clear)

    def get_text(self, locator):
        return self.driver.wait_for_element_and_get_text(locator)


    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def is_loaded(self, element):
        el = self.driver.wait_and_get_element(element, 2)
        if el is not None:
            return True
        else:
            return False

    def wait_for_redirect(self):
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.current_url == self.url)
        return self
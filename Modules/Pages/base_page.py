from functools import partial

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Modules.Helpers.javascript_helper import *
from Modules.Helpers.screenshot_helper import *
from Modules.Helpers.waiter_helper import *
from Tests.config import Config

class BasePage(object):

    timeout = Config.DEFAULT_TIMEOUT

    def __init__(self, driver: WebDriver):
        self.basic_url = self.url = Config.BASE_URL
        self.driver = driver
        self._initialize_methods()

    def _initialize_methods(self):
        self.remove_element = partial(remove_element, self.driver)
        self.scroll_to_height = partial(scroll_to_height, self.driver)
        self.scroll = partial(scroll, self.driver)
        self.get_inner_height = partial(get_inner_height, self.driver)
        self.get_entire_height = partial(get_entire_height, self.driver)
        self.get_screenshots_of_entire_page = partial(get_screenshots_of_entire_page, self.driver)

        self.wait_for_element = partial(wait_for_element, self.driver)
        self.wait_for_element_until_invisible = partial(wait_for_element_until_invisible, self.driver)
        self.wait_and_click_on = partial(wait_and_click_on, self.driver)
        self.wait_and_get_element = partial(wait_and_get_element, self.driver)
        self.wait_and_get_elements = partial(wait_and_get_elements, self.driver)
        self.wait_and_get_text = partial(wait_and_get_text, self.driver)
        self.wait_and_get_text_from_input = partial(wait_and_get_text_from_input, self.driver)
        self.wait_and_type = partial(wait_and_type, self.driver)
        self.wait_for_text = partial(wait_for_text, self.driver)

    def navigate(self):
        self.driver.get(self.url)
        return self

    def compare_url(self):
        if self.driver.current_url == self.url:
            return True
        else:
            return False

    def find_element(self, *locator):
        return self.driver.find_element(*locator)


    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def save_screenshot(self, file_name):
        entire_page_height = self.driver.execute_script("return document.body.scrollHeight")
        windows_height = self.driver.get_window_size()['height']

        self.driver.get_screenshot_as_file(("Screenshots/" + file_name + ".png"))

    def wait_for_redirect(self):
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.current_url == self.url)
        return self

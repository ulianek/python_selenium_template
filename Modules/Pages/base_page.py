from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Modules.Helpers.screenshot_helper import ScreenshotHelper
from Modules.Helpers.webdriver_extension import WebDriver
from Modules.config import Config


class BasePage(object):
    timeout = Config.DEFAULT_TIMEOUT

    def __init__(self, driver: WebDriver):
        self.basic_url = self.url = Config.BASE_URL
        self.driver = driver
        # self.screenshot_hp = ScreenshotHelper(self.driver)

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

    def click_on(self, locator, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(locator)
        )
        WebDriverWait(self, time).until(
            EC.element_to_be_clickable(locator)
        )
        self.find_element(*locator).click()

    def type(self, locator, text, time=Config.DEFAULT_WAIT_TIME, clear=True):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(locator)
        )
        if clear:
            self.find_element(*locator).clear()
        self.find_element(*locator).send_keys(text)

    def wait_for_text(self, element, text, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.text_to_be_present_in_element_value(element, text)
        )

    def wait_for_element(self, element, time=Config.DEFAULT_WAIT_TIME):
        try:
            WebDriverWait(self, time).until(
                EC.presence_of_element_located(element)
            )
        except:
            pass

    def wait_for_element_until_invisible(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.invisibility_of_element_located(element)
        )

    def element_is_invisible(self, element, time=timeout):
        self.wait_for_element(element, time)
        elements = self.find_elements(*element)
        if len(elements) > 0:
            return True
        else:
            return False

    def get_text(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element).text

    def get_text_from_input(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element).get_attribute("value")

    def get_element(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element)

    def get_elements(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_elements(*element)

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

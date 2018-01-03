from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Modules.Helpers.webdriver_extension import WebDriver


class BasePage(object):
    basic_url = "http://rentaware-dev.bitcraft.com.pl/"
    url = "http://rentaware-dev.bitcraft.com.pl/"

    ACCEPT_COOKIE_BTN = (By.ID, "acceptCookie")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)

    def compare_url(self):
        if self.driver.current_url == self.url:
            return True
        else:
            return False

    def wait_for_redirect(self):
        WebDriverWait(self.driver, 10).until(lambda driver: self.driver.current_url == self.url)

    def accept_cookies(self):
        try:
            self.driver.wait_for_element_and_click(self.ACCEPT_COOKIE_BTN, 3)
        except:
            pass

    def find_element(self, *locator):
        return self.driver.find_element(*locator)
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
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Modules.config import Config


class WebDriverMobile(WebDriver):
    def __init__(self, url, desired_caps):
        super().__init__(url, desired_caps)


    def wait_for_element_and_click(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        WebDriverWait(self, time).until(
            EC.element_to_be_clickable(element)
        )
        self.find_element(*element).click()

    def wait_for_element_and_send_text(self, element, text, time=Config.DEFAULT_WAIT_TIME, clear=True):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        if clear:
            self.find_element(*element).clear()
        self.find_element(*element).send_keys(text)

    def wait_for_text_in_element(self, element, text, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.text_to_be_present_in_element_value(element, text)
        )



    # def check_if_element_is_visible(self, element, time=15):
    #     try:
    #         WebDriverWait(self, time).until(
    #             EC.presence_of_element_located(element)
    #         )
    #         return True
    #     except TimeoutException:
    #         return False

    def check_if_element_is_invisible(self, element, time=Config.DEFAULT_WAIT_TIME):
        try:
            WebDriverWait(self, time).until(
                EC.invisibility_of_element_located(element)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_and_get_text(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element).text

    def wait_for_element_and_get_text_from_input(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element).get_attribute("value")

    def wait_and_get_element(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_element(*element)

    def wait_and_get_elements(self, element, time=Config.DEFAULT_WAIT_TIME):
        WebDriverWait(self, time).until(
            EC.presence_of_element_located(element)
        )
        return self.find_elements(*element)

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

    def check_if_element_is_visible(self, element, time=15):
        self.wait_for_element(element, 2)
        elements = self.find_elements(*element)
        if len(elements) > 0:
            return True
        else:
            return False
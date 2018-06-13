from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Tests.config import Config


def wait_and_click_on(driver, locator, time=Config.DEFAULT_TIMEOUT):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located(locator)
    )
    WebDriverWait(driver, time).until(
        EC.element_to_be_clickable(locator)
    )
    driver.find_element(*locator).click()


def wait_and_type(driver, locator, text, time=Config.DEFAULT_TIMEOUT, clear=True):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located(locator)
    )
    if clear:
        driver.find_element(*locator).clear()
        driver.find_element(*locator).send_keys(text)


def wait_for_text(driver, element, text, time=Config.DEFAULT_TIMEOUT):
    WebDriverWait(driver, time).until(
        EC.text_to_be_present_in_element_value(element, text)
    )


def wait_for_element(driver, element, time=Config.DEFAULT_TIMEOUT):
    try:
        WebDriverWait(driver, time).until(
            EC.presence_of_element_located(element)
        )
    except:
        pass


def wait_for_element_until_invisible(driver, element, time=Config.DEFAULT_TIMEOUT):
    WebDriverWait(driver, time).until(
        EC.invisibility_of_element_located(element)
    )


def wait_and_get_text(driver, element, time=Config.DEFAULT_TIMEOUT):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located(element)
    )
    return driver.find_element(*element).text


def wait_and_get_text_from_input(driver, element, time=Config.DEFAULT_TIMEOUT):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located(element)
    )
    return driver.find_element(*element).get_attribute("value")


def wait_and_get_element(driver, element, time=Config.DEFAULT_TIMEOUT):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located(element)
    )
    return driver.find_element(*element)


def wait_and_get_elements(driver, element, time=Config.DEFAULT_TIMEOUT):
    WebDriverWait(driver, time).until(
        EC.presence_of_element_located(element)
    )
    return driver.find_elements(*element)

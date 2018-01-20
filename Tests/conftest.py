from datetime import datetime
import os
import pytest
import pytz
from selenium import webdriver

from Modules.Helpers.webdriver_extension import WebDriver
from Modules.Helpers.webdriver_m_extension import WebDriverMobile
from Modules.Pages.base_page import BasePage
from Modules.config import Config


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--base_url", action="store", default="https://www.google.pl/?gws_rd=ssl",
                     help="Type in browser type")

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    try:
        driver = item.funcargs['driver']
        if report.when == 'call':
            screenshot = driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(screenshot, ''))
            xfail = hasattr(report, 'wasxfail')
            if (report.skipped and xfail) or (report.failed and not xfail):
                extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
            report.extra = extra
    except:
        pass


@pytest.fixture(scope='class')
def driver(request):
    Config.BASE_URL = request.config.getoption("--base_url")
    driver = WebDriver(request.config.getoption("--browser"))
    driver.maximize_window()
    base_page = BasePage(driver)
    base_page.navigate()

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver


@pytest.fixture(scope="class")
def mobile_driver():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '8.1.0'
    desired_caps['deviceName'] = "Nexus_5X_API_27_x86"
    desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exmaple.apk'))
    selenium_driver = WebDriverMobile('http://localhost:4723/wd/hub', desired_caps)

    yield selenium_driver

    selenium_driver.quit()


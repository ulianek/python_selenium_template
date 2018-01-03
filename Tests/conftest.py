import os
import pytest
from selenium import webdriver

from Modules.Helpers.webdriver_extension import WebDriver
from Modules.Pages.base_page import BasePage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser type")

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    driver = item.funcargs['driver']
    if report.when == 'call':
        screenshot = driver.get_screenshot_as_base64()
        extra.append(pytest_html.extras.image(screenshot, ''))
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        report.extra = extra


@pytest.fixture(autouse=True)
def driver(request):
    browser = request.config.getoption("--browser")
    driver = WebDriver(browser)
    driver.maximize_window()
    base_page = BasePage(driver)
    base_page.navigate()
    base_page.accept_cookies()

    yield driver

    driver.quit()
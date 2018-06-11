import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from Modules.Pages.base_page import BasePage
from Tests.config import Config


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--base_url", action="store", default="https://www.google.pl/?gws_rd=ssl",
                     help="Type in url")


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

@pytest.fixture(scope="class")
def screenshot_folder():
    path = Config.SCREENSHOTS_PATH
    if not os.path.exists(path):
        os.makedirs(path)

    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

@pytest.fixture(scope="class")
def clear_screenshots():
    folder = Config.SCREENSHOTS_PATH
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


@pytest.fixture(scope='class')
def driver(request):
    Config.BASE_URL = request.config.getoption("--base_url")
    browser = request.config.getoption("--browser")
    driver_web = None
    if browser == 'chrome':
        driver_web = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == 'firefox':
        driver_web = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        driver_web.maximize_window()
    base_page = BasePage(driver_web)
    base_page.navigate()

    def fin():
        driver_web.quit()

    request.addfinalizer(fin)
    return driver_web


@pytest.fixture(scope="class")
def mobile_driver():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '8.1.0'
    desired_caps['deviceName'] = "Nexus_5X_API_27_x86"
    desired_caps['browserName'] = "Chrome"
    # desired_caps['app'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exmaple.apk'))
    selenium_driver = WebDriverMobile('http://localhost:4723/wd/hub', desired_caps)

    yield selenium_driver

    selenium_driver.quit()

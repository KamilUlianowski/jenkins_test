import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Type in browser type")

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


@pytest.fixture(autouse=True)
def driver(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    yield driver

    driver.quit()
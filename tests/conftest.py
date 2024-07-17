import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser, support
import os

import config
from selene_in_action import utils

from appium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        '--device_name',
        default='Google Pixel 3'
    )
    parser.addoption(
        "--iosonly",
        type=bool,
        required=False,
        default=False,
    )
    parser.addoption(
        "--androidonly",
        type=bool,
        required=False,
        default=False,
    )


def pytest_collection_modifyitems(config, items: list[pytest.Item]):
    items.sort(key=lambda x: x.name, reverse=True)

    for item in items:
        if "ios" not in item.name and config.getoption("--iosonly"):
            item.add_marker(pytest.mark.skip("Мы запустили только ios тесты"))
        elif "android" not in item.name and config.getoption("--androidonly"):
            item.add_marker(pytest.mark.skip("Мы запустили только android тесты"))


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    device_name = request.config.getoption('--device_name')
    capabilities = {
        # Specify device and os_version for testing
        # 'platformName': 'android',
        # 'platformVersion': '9.0',
        'deviceName': device_name,

        # Set URL of the application under test
        'app': 'bs://sample.app',

        # Set other BrowserStack capabilities
        'bstack:options': {
            'projectName': 'First Python project',
            'buildName': 'browserstack-build-1',
            'sessionName': 'BStack first_test',

            # Set your access credentials
            'userName': config.bstack_userName,
            'accessKey': config.bstack_accessKey,
        }
    }
    if request.config.getoption('--androidonly'):
        options = UiAutomator2Options().load_capabilities(capabilities)
    elif request.config.getoption('--iosonly'):
        options = XCUITestOptions().load_capabilities(capabilities
                                                      #{
                                                      #"deviceName": "iPhone 11 Pro",
                                                      #"platformName": "ios",
                                                      #"platformVersion": "13",

                                                      # Set other BrowserStack capabilities
                                                      #'bstack:options': {
                                                      #    'projectName': 'First Python project',
                                                      #    'buildName': 'browserstack-build-1',
                                                      #    'sessionName': 'BStack first_test',
                                                      #   "app": "bs://sample.app",

                                                      # Set your access credentials
                                                      #   'userName': config.bstack_userName,
                                                      #   'accessKey': config.bstack_accessKey,
                                                      #}}
                                                      )
    else:
        print('unknown device')

    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            'http://hub.browserstack.com/wd/hub',
            options=options
        )

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    utils.allure.attach_bstack_video(session_id)

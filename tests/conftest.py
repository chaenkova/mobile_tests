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
        required=False,
        default='false',
    )
    parser.addoption(
        "--androidonly",
        required=False,
        default='true',
    )
    parser.addoption(
        "--context",
        required=False,
        default='bstack'
    )


def pytest_collection_modifyitems(config, items: list[pytest.Item]):
    items.sort(key=lambda x: x.name, reverse=True)

    for item in items:
        if ("ios" not in item.name) and (config.getoption("--iosonly").lower() == "true"):
            item.add_marker(pytest.mark.skip("Мы запустили только ios тесты"))
        elif ("android" not in item.name) and (config.getoption("--androidonly").lower() == "true"):
            item.add_marker(pytest.mark.skip("Мы запустили только android тесты"))


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    device_name = request.config.getoption('--device_name')
    context = request.config.getoption('--context')

    capabilities = config.to_driver_options(context=context, device_name=device_name)

    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options
    if context == 'bstack':
        if request.config.getoption('--androidonly').lower() == "true":
            options = UiAutomator2Options().load_capabilities(capabilities)
        elif request.config.getoption('--iosonly').lower() == "true":
            options = XCUITestOptions().load_capabilities(capabilities)
        else:
            print('unknown device')
    elif context == 'real_device':
        options = capabilities

    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(options.get_capability('remote_url'), options=options)

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield
    if context == 'bstack':
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

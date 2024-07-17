from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have
import time


def test_app_ios():
    with step('click text button'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Button")).click()
    with step('Type hello@browserstack.com'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Input")).send_keys("hello@browserstack.com" + "\n")
        time.sleep(5)
    with step('assert text in input'):
        text_output = browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Output"))
        if text_output.should(have.text("hello@browserstack.com")):
            assert True
        else:
            assert False

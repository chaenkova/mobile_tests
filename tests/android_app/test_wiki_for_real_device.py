from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


def test_search_android():
    with step('Find our language'):
        assert browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/option_label")).should(have.text('Русский'))

    with step('next screen'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")).click()

    with step('Verify content found'):
        assert browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")).should(have.text('Новые способы исследований'))

    with step('next screen'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")).click()

    with step('Verify content found'):
        assert browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")).should(have.text('Списки для чтения с синхронизацией'))

    with step('next screen'):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")).click()

    with step('Verify content found'):
        assert browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")).should(have.text('Данные и конфиденциальность'))

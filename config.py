import os
from dotenv import load_dotenv
from appium.options.android import UiAutomator2Options
from selene_in_action.utils.allure import path_from_project

base_url = os.getenv('base_url', 'https://www.wikipedia.org')


def to_driver_options(context, device_name):
    options = UiAutomator2Options()
    env_file_path = path_from_project(f".env.{context}.py")
    print(env_file_path)
    load_dotenv(dotenv_path=env_file_path)

    if context == 'real_device' or 'emulator':
        options.set_capability('remote_url', os.getenv('REMOTE_URL'))
        options.set_capability('deviceName', os.getenv('DEVICE_NAME'))
        options.set_capability('appWaitActivity', os.getenv('APP_WAIT_ACTIVITY'))
        options.set_capability('app', path_from_project(os.getenv('APP')))
    else:
        options = {
            # Specify device and os_version for testing
            # 'platformName': 'android',
            # 'platformVersion': '9.0',
            'deviceName': device_name,

            # Set URL of the application under test
            'app': 'bs://sample.app',
            'remote_url': 'http://hub.browserstack.com/wd/hub',

            # Set other BrowserStack capabilities
            'bstack:options': {
                'projectName': 'First Python project',
                'buildName': 'browserstack-build-1',
                'sessionName': 'BStack first_test',

                # Set your access credentials
                'userName': os.getenv('bstack_userName'),
                'accessKey': os.getenv('bstack_accessKey'),
            }
        }

    return options

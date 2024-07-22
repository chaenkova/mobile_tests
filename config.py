import os
from dotenv import load_dotenv
from appium.options.android import UiAutomator2Options
from selene_in_action.utils.file import path_from_project


def to_driver_options(context, device_name):
    options = UiAutomator2Options()
    env_file_path = path_from_project(f".env.{context}")
    load_dotenv(dotenv_path=env_file_path)

    if context == 'real_device' or context == 'emulator':
        options.set_capability('remote_url', os.getenv('REMOTE_URL'))
        options.set_capability('deviceName', os.getenv('DEVICE_NAME'))
        options.set_capability('appWaitActivity', os.getenv('APP_WAIT_ACTIVITY'))
        options.set_capability('app', path_from_project(os.getenv('APP')))
    else:
        options = {
            'deviceName': device_name,
            'remote_url': 'http://hub.browserstack.com/wd/hub',
            'app' :os.getenv('app'),

            'bstack:options': {
                'projectName': 'First Python project',
                'buildName': 'browserstack-build-1',
                'sessionName': 'BStack first_test',

                'userName': os.getenv('bstack_userName'),
                'accessKey': os.getenv('bstack_accessKey'),
            }
        }

    return options

import os

context = os.getenv('context', 'bstack')
bstack_userName = os.getenv('bstack_userName')
bstack_accessKey = os.getenv('bstack_accessKey')
base_url = os.getenv('base_url', 'https://www.wikipedia.org')
device_name = os.getenv('device_name','Google Pixel 3')
iosonly = os.getenv('iosonly',False)
androidonly = os.getenv('androidonly',False)
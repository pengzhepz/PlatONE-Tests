import os
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from setting import DRIVER, GLOBAL_TIMEOUT

drivers = {
    'chrome': webdriver.Chrome(chrome_options=webdriver.ChromeOptions()),
    # 'edge': webdriver.Edge(executable_path='msedgedriver.exe'),
    'ie': None,
    'firefox': None,
    'Safari': None,
    '...': None
}


@pytest.fixture(scope='session', autouse=False)
def driver() -> WebElement:
    driver = drivers[DRIVER]
    driver.maximize_window()
    driver.implicitly_wait(GLOBAL_TIMEOUT)
    yield driver
    # todo: 更换为更好的clean方法
    # os.system('taskkill /IM chromedriver.exe /F')
    # os.system('taskkill /IM chrome.exe /F')


def pytest_collection_modifyitems(items):
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")
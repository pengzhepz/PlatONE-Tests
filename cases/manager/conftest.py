from lib.mgrui.urls import ledger_url
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from lib.mgrui.locator.loginPage import LoginPage
from setting import DRIVER, GLOBAL_TIMEOUT
import time


# option = webdriver.ChromeOptions()
# option.add_argument('disable-infobars')  # 去掉正在监控中状态
drivers = {
    'chrome': webdriver.Chrome(),
    # 'edge': webdriver.Edge(executable_path='msedgedriver.exe'),
    'ie': None,
    'firefox': None,
    'Safari': None,
    '...': None
}

# 联盟后台登录账号
chain_ip = '192.168.120.133'
chain_port = '1331'
file = r'C:\Users\juzix\Downloads\lax1k388y5ewl5wq222w5ueg8efl64u06fz86rlev9.json'
file_pwd = '12345678'


@pytest.fixture(scope='session', autouse=False)
def driver() -> WebElement:
    driver = drivers[DRIVER]
    driver.maximize_window()
    driver.implicitly_wait(GLOBAL_TIMEOUT)
    yield driver
    # todo: 更换为更好的clean方法
    driver.close()
    # os.system('taskkill /IM chromedriver.exe /F')
    # os.system('taskkill /IM chrome.exe /F')


@pytest.fixture(scope='class')
def login(driver):
    """
    已登录页面
    """
    driver.get(ledger_url)
    lp = LoginPage(driver)
    lp.set_chain(chain_ip, chain_port)
    lp.login(file, file_pwd)
    time.sleep(2)
    return driver


def pytest_collection_modifyitems(items):
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")

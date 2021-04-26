import pytest
from lib.mgrui.urls import ledger_url
from lib.mgrui.locator.loginPage import LoginPage
from common.getYaml import get_data
import time


@pytest.fixture(scope='function')
def login_page(driver):
    driver.get(ledger_url)
    lp = LoginPage(driver)
    return lp


class TestLogin:
    """
    测试登录页面，done
    """
    cases, parameters = get_data(r'../../data/ui/login.yaml')  # 5条用例，各种身份登录

    @pytest.mark.skip()
    @pytest.mark.parametrize('params,expected', parameters, ids=cases)
    def test_login_success(self, login_page, params, expected):
        login_page.set_chain(params['ip'], params['port'])
        login_page.login(params['user'], params['pwd'], auth=params['auth'])
        time.sleep(2)
        assert expected['id'] == login_page.get_user_id()  # 判断首页身份

    def test_create_wallet_success(self, login_page):
        login_page.create_wallet(pwd='12345678', confirm_pwd='12345678')
        login_page.download_json()
        assert login_page.check_create_wallet() is True  # 判断“下一步”按钮是否点亮

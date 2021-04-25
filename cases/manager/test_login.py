import pytest
from lib.mgrui.urls import ledger_url
from lib.mgrui.locator.loginPage import LoginPage
from lib.mgrui.data.get_ui_data import get_data
import time


@pytest.fixture(scope='function')
def login_page(driver):
    driver.get(ledger_url)
    lp = LoginPage(driver)
    return lp


class TestLogin:
    cases, parameters = get_data(r'../../lib/mgrui/data/login.yaml')

    @pytest.mark.parametrize('params,expected', parameters, ids=cases)
    def test_login_success(self, login_page, params, expected):
        login_page.set_chain(params['ip'], params['port'])
        login_page.login(params['user'], params['pwd'], auth=params['auth'])
        time.sleep(2)
        assert expected['id'] == login_page.get_user_id()  # 判断首页身份

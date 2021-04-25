import time
import pytest
from lib.mgrui.urls import ledger_url
from lib.mgrui.userPage import UserPage
from lib.mgrui.loginPage import LoginPage
from lib.mgrui.data.get_ui_data import get_data


@pytest.fixture(scope='class')
def user_page(driver):
    driver.get(ledger_url)
    lp = LoginPage(driver)
    lp.set_chain('192.168.120.133', '1331')
    time.sleep(1)
    file = r'C:\Users\juzix\Desktop\lax19my0865mde2dlmujpa6l2z397mlwwrsn8lthur.json'
    lp.login(file, '12345678')
    lp.index(1)
    return UserPage(driver)


@pytest.mark.skip('pass')
class TestUser:
    cases, parameters = get_data(r'../../lib/mgrui/data/user.yaml')

    @pytest.mark.parametrize('params,expected', parameters, ids=cases)
    def test_add_user_success(self, user_page, params, expected):
        """
        TODO：用户管理页面的断言结果
        """

        user_page.add_user(params['name'], params['phone'], params['email'], params['address'], params['power'])

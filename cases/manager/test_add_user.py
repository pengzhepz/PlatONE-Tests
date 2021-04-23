import pytest
from lib.mgrui.urls import ledger_url
from lib.mgrui.userPage import UserPage
from lib.mgrui.loginPage import LoginPage
from lib.mgrui.data.get_ui_data import get_data


# @pytest.fixture(scope='function')
# def login_page(driver):
#     driver.get(ledger_url)
#     lp = LoginPage(driver)
#     return lp

@pytest.fixture(scope='function')
def user_page(driver):
    return UserPage(driver)


class TestUser:
    cases, parameters = get_data(r'../../lib/mgrui/data/user.yaml')


    @pytest.mark.parametrize('params,expected', parameters, ids=cases)
    def test_add_user_success(self,user_page,  params, expected):
        """
        TODO：用户管理页面的断言结果
        """

        user_page.add_user(params['name'], params['phone'], params['email'], params['address'], params['power'])
        assert expected['id'] is True

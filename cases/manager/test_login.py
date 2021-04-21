import pytest
from lib.mgrui.urls import login_url
from lib.mgrui import LoginPage


@pytest.fixture()
def login_page(driver):
    driver.get(login_url)
    lp = LoginPage(driver)
    return lp


class TestLogin:

    #  登录成功
    @pytest.mark.parametrize('username, password, authcode', [('admin', 'admin', '123456'), ('root', 'root', '888888')])
    def test_login_success(self, login_page, username, password, authcode):
        login_page.login(username, password, authcode)
        assert True

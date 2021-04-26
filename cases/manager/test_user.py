import pytest
from lib.mgrui.locator.userPage import UserPage


@pytest.fixture(scope='class')
def user_page(login):
    return UserPage(login)


class TestUser:
    # cases, parameters = get_data(r'../../lib/mgrui/data/user.yaml')

    @pytest.mark.parametrize('name,phone,email,address,power', [
        ('user100', '15820347777', '4477@qq.com', 'lax1knqnettnynusn08k2yg2uyzar6symvu6lpkw9c', '节点管理员')])
    def test_add_user_success(self, user_page, name, phone, email, address, power):
        """
        TODO：用户管理页面的断言结果
        """

        user_page.add_user(name, phone, email, address, power)

    def test_delete_user_success(self):
        pass

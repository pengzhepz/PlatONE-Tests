import pytest
from lib.mgrui.locator.userPage import UserPage


@pytest.fixture(scope='class')
def user_page(login):
    return UserPage(login)


class TestUser:
    """
    测试用户管理页面
    """

    @pytest.mark.parametrize('name,phone,email,address,power,expect', [
        ('user113', '15820347773', '447174@qq.com', 'lax1vf83f6yyzxqt6uerpfwcarvj9vtun8g4fdmkhq', '节点管理员', '新增用户成功!'),
        ('user112', '15820347773', '447174@qq.com', 'lax1vf83f6yyzxqt6uerpfwcarvj9vtun8g4fdmkhq', '游客', '用户地址已经注册')])
    def test_01_add_user_success(self, user_page, name, phone, email, address, power, expect):
        """
        添加用户
        """
        user_page.add_user(name, phone, email, address, power)
        assert user_page.check_text(expect) is True

    def test_03_delete_user_success(self, user_page):
        """
        删除用户
        """
        user_page.delete_user(index=0)  # 删除第1个用户
        assert user_page.check_text('用户信息删除成功!') is True

    def test_04_edit_user(self, user_page):
        """
        修改用户
        """
        user_page.edit_user()
        user_page.choose_power('节点管理员')
        assert user_page.check_text('更新用户信息成功!') is True

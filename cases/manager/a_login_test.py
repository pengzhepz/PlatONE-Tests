import pytest
from lib.mgrui.urls import ledger_url
from lib.mgrui.loginPage import LoginPage
import os
import time


@pytest.fixture(scope='function')
def login_page(driver):
    driver.get(ledger_url)
    lp = LoginPage(driver)
    return lp


class TestLogin:
    """
    测试登录页面
    """
    user_path = os.path.abspath(os.path.join(os.getcwd(), "../../files/"))

    @pytest.mark.skip('不能重复创建同样数据的链')
    def test_01_create_chain(self, login_page):
        """
        创建链
        TODO: 断言
        """
        try:
            login_page.create_chain_1()
            login_page.create_chain_2(script='/linux/scripts', ip='192.168.120.133', rpc='1331',
                                      file=r'C:\Users\juzix\Documents\platone-license', user='juzix', desc='webauto',
                                      p2pport='11331', host='192.168.120.133', pwd='123456')
            assert login_page.check_text('加入') is False
        finally:
            pass
            """
            from common.connectServer import connect_linux
            print('开始清理数据......')
            s = connect_linux('192.168.120.13','juzix','123456')  # TODO： 敏感信息不暴露
            stdin, stdout, stderr = s.exec_command(f'cd ~/linux && rm -rf data/ conf/genesis.json platone-license')
            stdin2, stdout2, stderr2 = s.exec_command(f'killall -9 platone')
            # result = str(stdout.read(), encoding='utf-8')
            # print(result)
            """

    @pytest.mark.parametrize("user,pwd,auth,ip,port,expect", [
        (user_path + '\\chaincreater.json', 12345678, True, '192.168.120.133', '7789', '链创建者'),
        (user_path + '\\chainmanager.json', 12345678, True, '192.168.120.133', '7789', '链管理员'),
        (user_path + '\\nodemanager.json', 12345678, True, '192.168.120.133', '7789', '节点管理员'),
        (user_path + '\\contractmanager.json', 12345678, True, '192.168.120.133', '7789', '合约管理员'),
        (user_path + '\\nodepublicter.json', 12345678, True, '192.168.120.133', '7789', '合约部署员'),
        (user_path + '\\visitor.json', 12345678, True, '192.168.120.133', '7789', '游客')
    ])
    def test_02_login_success(self, login_page, user, pwd, auth, ip, port, expect):
        """
        不同角色之间的登录
        """
        login_page.set_chain(ip, port)
        login_page.login(user, pwd)
        time.sleep(2)
        assert expect == login_page.get_user_id()  # 判断首页身份

    def test_03_create_wallet_success(self, login_page):
        """
        创建钱包
        """
        login_page.create_wallet(pwd='12345678', confirm_pwd='12345678')
        login_page.download_json()
        assert login_page.check_create_wallet() is True  # 判断“下一步”按钮是否点亮

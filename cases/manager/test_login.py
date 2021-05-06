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

    @pytest.mark.parametrize('params,expected', parameters, ids=cases)
    def test_login_success(self, login_page, params, expected):
        """
        不同角色之间的登录
        """
        login_page.set_chain(params['ip'], params['port'])
        login_page.login(params['user'], params['pwd'], auth=params['auth'])
        time.sleep(2)
        assert expected['id'] == login_page.get_user_id()  # 判断首页身份

    def test_create_wallet_success(self, login_page):
        """
        创建钱包
        """
        login_page.create_wallet(pwd='12345678', confirm_pwd='12345678')
        login_page.download_json()
        assert login_page.check_create_wallet() is True  # 判断“下一步”按钮是否点亮

    def test_create_chain(self, login_page):
        """
        创建链
        TODO: 测试数据有问题，链已存在 && 数据清理
        """
        try:
            login_page.create_chain_1()
            login_page.create_chain_2(script='/linux/scripts', ip='192.168.120.133', rpc='1331',
                                      file=r'C:\Users\juzix\Documents\platone-license', user='juzix', desc='webauto',
                                      p2pport='11331', host='192.168.120.133', pwd='123456')
            # assert login_page.check_text('') is True
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
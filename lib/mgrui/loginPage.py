import time
from .basePage import BasePage
from .locator import LoginLocator as loc
import os


class LoginPage(BasePage):

    def get_login_errormsg(self):
        self.wait_eleVisible(loc.login_errormsg_txt, mark='等待登陆错误提示出现')
        msg = self.get_Text(loc.login_errormsg_txt, mark='获取登陆错误提示信息')
        return msg

    def get_title(self):
        title = self.get_Text(loc.title_txt, mark='获取页面title')
        return title

    def login(self, username, pwd, auth=True):
        self.click_Element(loc.select_user, mark='上传json文件')
        time.sleep(2)
        path = os.path.abspath('..') + '\\uploadjson.exe'  # 上传文件
        os.system(fr'{path} {username}')
        self.input_Text(loc.password_input, pwd, mark='输入密码')
        if auth:
            pass
        else:
            self.choose_auth()
        self.click_Element(loc.login_button, mark='登录')

    def set_chain(self, ip, port):
        self.click_Element(loc.set_chain, mark='配置链')
        self.input_Text(loc.ip_address, ip, mark='设置ip')
        self.input_Text(loc.rpc_port, port, mark='设置端口号')
        self.click_Element(loc.connect_chain, mark='连接链')
        time.sleep(1)

    def choose_auth(self):
        self.click_Element(loc.select_auth, mark='选择是/否国密')
        self.click_Element(loc.no_auth, mark='选择不使用国密')

    def get_user_id(self):
        return self.get_Text(loc.user_id, mark='用户者身份')

    def log_out(self):
        self.click_Element(loc.logout)
        self.click_Element(loc.logout_2, mark='退出登录')
        time.sleep(1)

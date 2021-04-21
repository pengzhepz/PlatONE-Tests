from .basePage import BasePage
from .locator import LoginLocator as loc


class LoginPage(BasePage):

    def login(self, username, password, authcode):
        self.clean_Input_Text(loc.username_input, mark='清除页面记录的用户名')
        self.input_Text(loc.username_input, username, mark='输入用户名')
        self.clean_Input_Text(loc.password_input, mark='清除页面记录的密码')
        self.input_Text(loc.password_input, password, mark='输入密码')
        self.input_Text(loc.authcode_input, authcode, mark='输入验证码')
        self.click_Element(loc.login_button, mark='点击登陆按钮')

    def get_login_errormsg(self):
        self.wait_eleVisible(loc.login_errormsg_txt, mark='等待登陆错误提示出现')
        msg = self.get_Text(loc.login_errormsg_txt, mark='获取登陆错误提示信息')
        return msg

    def get_title(self):
        title = self.get_Text(loc.title_txt, mark='获取页面title')
        return title

    def get_url(self):
        title = self.browser.current_url(loc.title_txt, mark='获取页面title')
        return title

import time
from .basePage import BasePage
from .locator.usermanger import UserMangerLocator as loc


class UserPage(BasePage):

    def add_user(self, name, phone, email, address, power):
        self.click_Element(loc.add_user, mark='添加用户')
        time.sleep(1)
        self.input_Text(loc.name, name, mark='输入用户名')
        self.input_Text(loc.phone, phone, mark='输入电话号码')
        self.input_Text(loc.email, email, mark='输入电子邮箱')
        self.input_Text(loc.address, address, mark='输入地址')
        self.choose_power(power)
        self.click_Element(loc.submit_btn)
        time.sleep(5)

    def choose_power(self, power):
        self.click_Element(loc.power)
        self.click_Text(power, mark='选择权限')

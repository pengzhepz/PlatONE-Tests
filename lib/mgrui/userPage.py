import time
from .basePage import BasePage
from selenium.webdriver.common.by import By


class UserPage(BasePage):
    """
    添加用户页面
    """
    add_user_btn = (By.CLASS_NAME, 'anticon-plus')
    user_name_input = (By.ID, 'normal_login_name')
    user_phone_input = (By.ID, 'normal_login_mobile')
    user_email_input = (By.ID, 'normal_login_email')
    user_address_input = (By.ID, 'normal_login_address')
    select_user_auth_btn = (By.CLASS_NAME, 'ant-select-selection-item')
    submit_btn = (By.CLASS_NAME, 'submit_btn')
    edit_user_btn = (By.XPATH, '//*[text()="修改"]')
    delete_user_btn = (By.XPATH, '//*[text()="删除"]')
    userManger = (By.XPATH, '//*[text()="用户管理"]')

    def add_user(self, name, phone, email, address, power):
        """
        添加用户的数据
        """
        self.select_user_index()
        self.click_Element(self.add_user_btn, mark='添加用户')
        time.sleep(1)
        self.input_Text(self.user_name_input, name, mark='输入用户名')
        self.input_Text(self.user_phone_input, phone, mark='输入电话号码')
        self.input_Text(self.user_email_input, email, mark='输入电子邮箱')
        self.input_Text(self.user_address_input, address, mark='输入地址')
        self.choose_power(power)

    def choose_power(self, power):
        """
        选择用户角色
        """
        self.click_Element(self.select_user_auth_btn)
        time.sleep(1)
        self.click_Text(power, mark='选择权限')
        self.click_Element(self.submit_btn)

    def select_user_index(self):
        self.click_Element(self.userManger, mark='选择用户管理页卡')

    def delete_user(self, index):
        # 删除用户
        self.select_user_index()
        user_list = self.find_Elements(self.delete_user_btn)
        user_list[index].click()
        time.sleep(1)
        self.click_Text('确 认')
        time.sleep(1)

    def edit_user(self, index=1):
        # 修改用户
        self.select_user_index()
        user_list = self.find_Elements(self.edit_user_btn)
        user_list[index].click()
        time.sleep(1)



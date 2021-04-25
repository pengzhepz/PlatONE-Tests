import time
from .basePage import BasePage
from .locator.billmanger import BiilMangerLocator as loc
from selenium.webdriver.common.by import By


class BillPage(BasePage):

    def add_bill(self, name, index):
        self.click_Element(loc.add_bill, mark='点击添加账本')
        self.input_Text(loc.bill_name, name, mark='输入账本名字')
        self.choice_node(index)
        self.click_Element(loc.submit, mark='提交')
        time.sleep(5)

    def add_sub_node(self):
        self.click_Element(loc.add_sub_node, mark='添加子节点')

    def close_bill(self, index):
        y = (By.XPATH,
             f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[{index}]/td[5]/div/div[2]/span/span')
        self.click_Element(y, mark='关闭账本')
        # print(self.driver.page_source)
        self.click_Text('确 认')

    def choice_node(self, index):
        x = (By.XPATH, f'//*[@id="normal_login_nodes"]/div/div/table/tbody/tr[{index}]/td[3]/div/div/span/span')
        self.click_Element(x, mark='选择节点')

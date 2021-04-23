import os, time
from .basePage import BasePage
from .locator.billmanger import BiilMangerLocator as loc


class BillPage(BasePage):

    def add_bill(self,name):
        self.click_Element(loc.add_bill, mark='点击添加账本')
        self.input_Text(loc.bill_name,name, mark='输入账本名字')
        self.click_Element(loc.add_bill_node, mark='添加节点')
        self.click_Element(loc.submit, mark='提交')

    def add_sub_node(self):
        self.click_Element(loc.add_sub_node,mark='添加子节点')

    def close_bill(self):
        self.click_Element(loc.closs_bill_node,mark='关闭账本')
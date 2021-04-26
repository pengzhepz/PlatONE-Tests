import time
from basePage import BasePage
from selenium.webdriver.common.by import By


class LedgerPage(BasePage):
    """
    账本页面
    """

    add_ledger_btn = (By.CLASS_NAME, 'anticon-plus')
    ledger_name_input = (By.ID, 'normal_login_ledgerName')
    ledger_node_btn = (By.CLASS_NAME, 'ant-space-align-center')
    submit_btn = (By.CLASS_NAME, 'submit_btn')
    add_sub_node_btn = (By.XPATH,
                        '//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]/div/div[1]/span/span')
    close_ledger_btn = (By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div[2]/button[2]/span')

    ledgerManger = (By.XPATH, '//*[text()="账本管理"]')

    def add_ledger(self, name, index):
        """
        添加账本
        """
        self.click_Element(self.add_ledger, mark='点击添加账本')
        self.input_Text(self.ledger_name_input, name, mark='输入账本名字')
        self.choice_node(index)
        self.click_Element(self.submit_btn, mark='提交')
        time.sleep(5)

    def choice_node(self, index):
        """
        创建账本，选择节点加入账本
        """
        choice_node_btn = (
            By.XPATH, f'//*[@id="normal_login_nodes"]/div/div/table/tbody/tr[{index}]/td[3]/div/div/span/span')
        self.click_Element(choice_node_btn, mark='选择节点')

    def add_sub_node(self):
        """
        账本中添加子节点
        """
        self.click_Element(self.add_sub_node, mark='添加子节点')

    def close_ledger(self, index):
        """
        关闭账本
        """
        ledger_close_btn = (By.XPATH,
                            f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[{index}]/td[5]/div/div[2]/span/span')
        self.click_Element(ledger_close_btn, mark='关闭账本')
        self.click_Text('确 认')

    def select_ledger_index(self):
        self.click_Element(self.ledgerManger,mark='选择账本管理页卡')

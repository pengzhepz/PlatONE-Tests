import time
from .basePage import BasePage
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
    choice_add_node_btn = (By.XPATH, '//*[text()="添加"]')
    ledgerManger = (By.XPATH, '//*[text()="账本管理"]')

    def add_ledger(self, name, index=0):
        """
        添加账本
        """
        self.select_ledger_index()
        time.sleep(1)
        self.click_Text('新建账本', mark='点击添加账本')
        self.input_Text(self.ledger_name_input, name, mark='输入账本名字')
        node_list = self.find_Elements(self.choice_add_node_btn)
        node_list[index].click()
        self.click_Text('提 交')

    def choice_node(self, index):
        """
        创建账本，选择节点加入账本(停用)
        """
        self.select_ledger_index()
        choice_node_btn = (
            By.XPATH, f'//*[@id="normal_login_nodes"]/div/div/table/tbody/tr[{index}]/td[3]/div/div/span/span')
        self.click_Element(choice_node_btn, mark='选择节点')

    def add_sub_node(self):
        """
        账本中添加子节点
        """
        self.select_ledger_index()
        self.click_Element(self.add_sub_node, mark='添加子节点')

    def close_ledger(self, index=1):
        """
        关闭账本
        """
        self.select_ledger_index()
        ledger_close_btn = (By.XPATH,
                            f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[{index}]/td[5]/div/div[2]/span/span')
        self.click_Element(ledger_close_btn, mark='关闭账本')
        self.click_Text('确 认')

    def select_ledger_index(self):
        self.click_Element(self.ledgerManger, mark='选择账本管理页卡')

    def check_add_node_fail(self, text):
        x = (By.XPATH, f'//*[text()="{text}"]')
        return self.wait_eleVisible(x)

    def add_all(self, name):
        """
        添加账本,添加所有已有的节点
        """
        # from selenium.webdriver.remote.webelement import WebElement
        self.select_ledger_index()
        time.sleep(1)
        self.click_Text('新建账本', mark='点击添加账本')
        self.input_Text(self.ledger_name_input, name, mark='输入账本名字')
        node_list = self.find_Elements(self.choice_add_node_btn)
        for i in node_list:
            # if isinstance(WebElement, i):  # 判断是否是可用元素
            i.click()
        self.click_Text('提 交')

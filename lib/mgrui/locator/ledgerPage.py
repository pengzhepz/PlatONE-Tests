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
        index: 指定哪一个
        """
        self.select_ledger_index()
        self.click_Text('新建账本', mark='点击添加账本')
        self.input_Text(self.ledger_name_input, name, mark='输入账本名字')
        node_list = self.find_Elements(self.choice_add_node_btn)
        time.sleep(1)
        node_list[index].click()
        self.click_Text('提 交')

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
        time.sleep(1)
        self.click_Text('确 认')

    def select_ledger_index(self):
        self.click_Element(self.ledgerManger, mark='选择账本管理页卡')
        time.sleep(1)

    def add_specify_node(self, name, start=None, end=None, auto=True):
        """
        添加账本,添加特定范围的节点
        usage:[1,3]，添加第2个、第3个节点
        auto: False不添加任何节点
        """
        self.select_ledger_index()
        self.click_Text('新建账本', mark='点击添加账本')
        self.input_Text(self.ledger_name_input, name, mark='输入账本名字')
        if auto:
            node_list = self.find_Elements(self.choice_add_node_btn)
            for i in node_list[start:end]:
                time.sleep(1)
                # from selenium.webdriver.remote.webelement import WebElement
                # if isinstance(WebElement, i):  # 判断是否是可用元素
                i.click()
        else:
            pass
        self.click_Text('提 交')

    def enter_ledger_detail(self, index=1):
        """
        进入账本详情页
        """
        self.select_ledger_index()
        x = (By.XPATH,
             f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[{index}]/td[2]/a')
        self.click_Element(x, mark=f'点击第{index}个账本名，进入详情页')

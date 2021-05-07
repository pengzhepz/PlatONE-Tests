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
    new_ledger_node_btn = (By.XPATH, '//*[text()="新增节点"]')
    delete_btn = (By.XPATH, '//*[text()="删除"]')
    to_public_btn = (By.XPATH, '//*[text()="修改为共识节点"]')
    to_normal_btn = (By.XPATH, '//*[text()="修改为观察者节点"]')

    auth_btn = (By.XPATH, '//*[@id="root"]/div/section/section/div/div/main/div/div/div[1]/div[2]/div/div[2]/button')
    re_auth_btn = (By.XPATH, '//*[@id="root"]/div/section/section/div/div/main/div/div/div[1]/div[2]/div/div[3]/button')
    close_btn = (By.CLASS_NAME, 'ant-modal-close-x')

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
        time.sleep(3)  # 初始化要时间
        x = (By.XPATH,
             f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[{index}]/td[2]/a')
        self.click_Element(x, mark=f'点击第{index}个账本名，进入详情页')

    def add_ledger_node(self, num=1):
        """
        进入账本详情页--添加节点
        :num ：添加节点的个数，至少1
        """
        self.click_Text("新增节点", mark='账本添加子节点')
        node_list = self.find_Elements(self.choice_add_node_btn)
        try:
            for i in range(num):
                node_list[i].click()
        except IndexError as e:
            print('个数越界！', e)

    def modify_2pulicnode(self, num=1):
        """
        账本中，修改观察者节点为共识节点
        """
        node_list = self.find_Elements(self.to_public_btn, mark='找有多少个修改共识节点数')
        try:
            for i in range(num):
                node_list[i].click()
                self.click_Text('确 认')
        except IndexError as e:
            print('个数越界！', e)

    def modify_2noramlnode(self, num=1):
        """
        账本中，修改共识节点为观察者节点
        """
        node_list = self.find_Elements(self.to_normal_btn, mark='找有多少个修改观察者节点数')
        try:
            for i in range(num):
                node_list[i].click()
                x = (By.XPATH, '//*[text()="共识节点数量不能小于节点列表数量的2/3"]')
                if self.wait_eleVisible(x, timeout=5):
                    print('====>共识节点数量不能小于节点列表数量的2/3<====')
                    raise
                else:
                    self.click_Text('确 认')
        except IndexError as e:
            print('个数越界！', e)

    def delete_node(self, num):
        """
        删除账本中的观察者节点
        """
        node_list = self.find_Elements(self.delete_btn, mark='找有多少个可删除节点数')
        try:
            for i in range(num):
                node_list[i].click()
                self.click_Text('确 认')
        except IndexError as e:
            print('个数越界！', e)

    def authorize(self, index=1):
        """
        授权
        """
        self.click_Element(self.auth_btn, mark='授权')
        time.sleep(1)
        if index == 1:
            x = (By.XPATH,
                 f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[4]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div/div/table/tbody/tr/td[3]/div/div/span/span')
        else:
            x = (By.XPATH,
                 f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[4]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div/div/table/tbody/tr[{index}]/td[3]/div/div/span/span')
        self.click_Element(x)

    def re_authorize(self, index=1):
        """
        回收权限
        """
        self.click_Element(self.re_auth_btn, mark='回收权限')
        time.sleep(1)
        if index == 1:
            x = (By.XPATH,
                 f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[4]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div/div/table/tbody/tr/td[3]/div/div/span/span')
        else:
            x = (By.XPATH,
                 f'//*[@id="root"]/div/section/section/div/div/main/div/div/div[4]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div/div/table/tbody/tr[{index}]/td[3]/div/div/span/span')
        self.click_Element(x)

    def close_ledger_window(self):
        # 关闭新建账本窗口按钮
        self.click_Element(self.close_btn)

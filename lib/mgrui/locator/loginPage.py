import time
from basePage import BasePage
from selenium.webdriver.common.by import By
import os


class LoginPage(BasePage):
    """
    登录页面
    """

    # 登录页面
    select_user_btn = (By.CLASS_NAME, 'select_btn')
    username_input = (By.ID, 'normal_login_username')
    password_input = (By.ID, 'normal_login_password')
    select_auth_btn = (By.CLASS_NAME, 'ant-select-selector')
    no_auth = (By.XPATH, '//*[text()="不使用国密"]')
    login_button = (By.CLASS_NAME, 'login-form-button')
    register_user_btn = (By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/p[1]/span')
    create_wallet_btn = (By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/p[2]/span')

    # 配置链
    set_chain_btn = (By.CLASS_NAME, 'chain_btn')
    ip_address = (By.ID, 'connent_box_ip')
    rpc_port = (By.ID, 'connent_box_port')
    connect_chain = (By.CLASS_NAME, 'connent_box_button')

    # 创建钱包页面
    new_wallet_pwd = (By.ID, 'walletForm_password')
    new_wallet_confirm_pwd = (By.ID, 'walletForm_checkPassword')
    complete_create_wallet_btn = (By.XPATH, '//*[@id="walletForm"]/div[4]/button')
    download_address_btn = (By.CLASS_NAME, 'ml10')
    next_btn = (By.XPATH, '//*[@id="root"]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[3]/button')

    # 创建链页面
    script_path = (By.ID, 'chainForm_scriptPath')
    nodeIp = (By.ID, 'chainForm_nodeIp')
    chain_rpc = (By.ID, 'chainForm_rpcPort')
    license = (By.XPATH, 'ant-input-search-button')
    useDock = (By.CLASS_NAME, 'ant-select-selection-item')
    chain_user = (By.ID, 'chainForm_userName')
    genesis_address = (By.ID, 'chainForm_creatorAddress')
    desc = (By.ID, 'chainForm_nodeDesc')
    nodep2p = (By.ID, 'chainForm_p2pPort')
    server_ip = (By.ID, 'chainForm_serverIp')
    chain_pwd = (By.ID, 'chainForm_password')
    start_create_chain = (By.XPATH, '//*[@id="chainForm"]/div[7]/button')

    # 首页list+退出登录
    home = (By.XPATH, '//*[text()="首页"]')
    userManger = (By.XPATH, '//*[text()="用户管理"]')
    nodeManger = (By.XPATH, '//*[text()="节点管理"]')
    dealManger = (By.XPATH, '//*[text()="账本管理"]')
    camera = (By.XPATH, '//*[text()="监控"]')

    logout_btn = (By.CLASS_NAME, 'avatar')
    confirm_logout_btn = (By.XPATH, '/html/body/div[3]/div/div/ul/li/a')

    # 检测元素
    user_id = (By.XPATH, '//*[@id="root"]/div/section/section/div/div/main/div/div/div/div[2]/div[1]/div[4]')

    def login(self, username, pwd, auth=True):
        """
        登录
        """
        self.click_Element(self.select_user_btn, mark='上传json文件')
        time.sleep(1)
        path = os.path.abspath('../..') + '\\uploadjson.exe'  # 上传文件
        os.system(fr'{path} {username}')
        self.input_Text(self.password_input, pwd, mark='输入密码')
        if auth:
            pass
        else:
            self.choose_no_auth()
        self.click_Element(self.login_button, mark='登录')

    def set_chain(self, ip, port):
        """
        配置链
        """
        self.click_Element(self.set_chain_btn, mark='配置链')
        self.input_Text(self.ip_address, ip, mark='设置ip')
        self.input_Text(self.rpc_port, port, mark='设置端口号')
        time.sleep(0.5)
        self.click_Element(self.connect_chain, mark='连接链')
        time.sleep(1)

    def choose_no_auth(self):
        """
        不使用国密
        """
        self.click_Element(self.select_auth_btn, mark='选择是/否国密')
        self.click_Element(self.no_auth, mark='选择不使用国密')

    def get_user_id(self):
        """
        获取用户身份TEXT
        """
        return self.get_Text(self.user_id, mark='用户者身份')

    def log_out(self):
        """
        登出用户
        """
        self.click_Element(self.logout_btn)
        self.click_Element(self.confirm_logout_btn, mark='退出登录')
        time.sleep(1)

    def index(self, index):
        """
        点击登录后首页的左侧列表
        :param index: 第几个（从0开始）
        :return:
        """
        li = [self.home, self.userManger, self.nodeManger, self.dealManger, self.camera]
        self.click_Element(li[index], mark='点击首页列表')

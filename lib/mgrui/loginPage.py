import time
from .basePage import BasePage
from selenium.webdriver.common.by import By


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
    create_chain_btn = (By.XPATH, '//*[text()="创建链"]')

    # 创建钱包页面
    new_wallet_pwd = (By.ID, 'walletForm_password')
    new_wallet_confirm_pwd = (By.ID, 'walletForm_checkPassword')
    complete_create_wallet_btn = (By.XPATH, '//*[@id="walletForm"]/div[4]/button')
    download_address_btn = (By.CLASS_NAME, 'ml10')
    next_btn = (By.XPATH, '//*[@id="root"]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[3]/button')

    # 创建链页面
    script_path_input = (By.ID, 'chainForm_scriptPath')
    nodeIp_input = (By.ID, 'chainForm_nodeIp')
    chain_rpc_input = (By.ID, 'chainForm_rpcPort')
    license_input = (By.XPATH, '//*[text()="上 传"]')
    useDock_input = (By.CLASS_NAME, 'ant-select-selection-item')
    chain_user_input = (By.ID, 'chainForm_userName')
    genesis_address_input = (By.ID, 'chainForm_creatorAddress')
    desc_input = (By.ID, 'chainForm_nodeDesc')
    nodep2p_input = (By.ID, 'chainForm_p2pPort')
    server_ip_input = (By.ID, 'chainForm_serverIp')
    chain_pwd_input = (By.ID, 'chainForm_password')
    start_create_chain_btn = (By.XPATH, '//*[@id="chainForm"]/div[7]/button')

    home = (By.XPATH, '//*[text()="首页"]')

    logout_btn = (By.CLASS_NAME, 'avatar')
    confirm_logout_btn = (By.XPATH, '/html/body/div[3]/div/div/ul/li/a')

    # 检测元素
    user_id = (By.XPATH, '//*[@id="root"]/div/section/section/div/div/main/div/div/div/div[2]/div[1]/div[4]')

    def login(self, username, pwd, auth=True):
        """
        登录
        """
        self.upload_file(self.select_user_btn, username)
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

    def create_wallet(self, pwd=12345678, confirm_pwd=12345678):
        """
        1.创建链
        2.创建用户
        """
        self.click_Element(self.set_chain_btn, mark='配置链')
        time.sleep(0.5)
        self.click_Element(self.create_chain_btn, mark='创建链')
        self.input_Text(self.new_wallet_pwd, pwd, mark='输入第一次密码')
        self.input_Text(self.new_wallet_confirm_pwd, confirm_pwd, mark='输入二次密码')
        time.sleep(1)
        self.click_Element(self.complete_create_wallet_btn, mark='创建用户')
        # self.clean_Text('创建钱包')

    def download_json(self):
        """
        下载用户json文件
        """
        self.click_Element(self.download_address_btn, mark='下载json文件')
        time.sleep(2)

    def check_create_wallet(self):
        """
        下载json文件后，检查“下一步”是否点亮
        """
        return self.is_Enabled(self.next_btn, mark='下一步是否点亮')

    def create_chain_1(self):
        """
        创建链step1:创建钱包，并下载创世地址json
        """
        self.create_wallet()  # 创建钱包
        self.download_json()
        self.click_Element(self.next_btn, mark='下一步')

    def create_chain_2(self, script, ip, rpc, file, user, desc, p2pport, host, pwd, usedocker=False):
        """
        创建链step2：初始化链
        """
        self.input_Text(self.script_path_input, script, mark='输入链部署路径')
        self.input_Text(self.nodeIp_input, ip, mark='输入节点ip')
        self.input_Text(self.chain_rpc_input, rpc, mark='输入rpc端口')
        self.upload_file(self.license_input, file)
        if usedocker:
            pass
        else:
            self.click_Text('是', mark='选择是/否docker部署')
            self.click_Text('否', mark='选择否docker部署')
        self.input_Text(self.chain_user_input, user, mark='输入服务器用户名')
        self.input_Text(self.desc_input, desc, mark='输入链描述')
        self.input_Text(self.nodep2p_input, p2pport, mark='输入p2p端口')
        self.input_Text(self.server_ip_input, host, mark='输入服务器ip')
        self.input_Text(self.chain_pwd_input, pwd, mark='输入服务器密码')
        self.click_Element(self.start_create_chain_btn, mark='初始化链')
        # time.sleep(30)

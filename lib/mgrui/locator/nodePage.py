import time
from .basePage import BasePage
from selenium.webdriver.common.by import By


class NodePage(BasePage):
    """
    添加节点页面
    """
    add_node_btn = (By.CLASS_NAME, 'anticon-plus')
    node_name_input = (By.ID, 'normal_login_name')
    node_desc_input = (By.ID, 'normal_login_desc')
    node_rpc_input = (By.ID, 'normal_login_rpcPort')
    docker_choice_btn = (By.CLASS_NAME, 'ant-select-selection-item')
    license_file = (
        By.XPATH, '//*[@id="normal_login"]/div[4]/div[2]/div[1]/div/div[2]/div[1]/div/span/span/span/button')
    server_ip_input = (By.ID, 'normal_login_ip')
    server_pwd_input = (By.ID, 'normal_login_password')
    node_type_input = (By.XPATH, '//*[@id="normal_login"]/div[1]/div[2]/div/div[2]/div/div/div/span')
    node_host_input = (By.ID, 'normal_login_hostAddress')
    node_p2pport_input = (By.ID, 'normal_login_p2pPort')
    genesis_file = (By.XPATH, '//*[@id="normal_login"]/div[4]/div[1]/div[2]/div/div[2]/div/div/span/span/span/button')
    node_script_input = (By.ID, 'normal_login_scriptPath')
    server_user_input = (By.ID, 'normal_login_userName')
    submit_btn = (By.XPATH, '//*[@id="normal_login"]/div[5]/button')

    # 节点操作
    edit_btn = (By.XPATH, '//*[text()="修改"]')
    edit_public_btn = (By.XPATH, '//*[text()="修改为共识节点"]')
    edit_normal_btn = (By.XPATH, '//*[text()="修改为观察者节点"]')
    stop_btn = (By.XPATH, '//*[text()="禁用"]')
    delete_btn = (By.XPATH, '//*[text()="删除"]')
    start_btn = (By.XPATH, '//*[text()="启用"]')
    edit_submit_btn = (By.XPATH, '//*[@id="normal_login"]/div[4]/button')
    nodeManger = (By.XPATH, '//*[text()="节点管理"]')

    def add_node(self, name, desc, rpc, license_file, ip, pwd, host, p2pport, genesis_file, script, user,
                 docker=False):
        """
        添加节点的数据
        """
        self.select_node_index()
        self.click_Element(self.add_node_btn)
        time.sleep(1)
        self.input_Text(self.node_name_input, name, mark='输入节点名称')
        self.input_Text(self.node_desc_input, desc, mark='节点说明')
        self.clean_Text(self.node_rpc_input)
        self.input_Text(self.node_rpc_input, rpc, mark='rpc端口')
        if docker:
            pass
        else:
            self.click_Text('是', mark='选择是/否docker部署')
            self.click_Text('否', mark='选择否docker部署')
        self.upload_file(self.license_file, license_file)
        self.input_Text(self.server_ip_input, ip, mark='输入服务器ip')
        self.input_Text(self.server_pwd_input, pwd, mark='输入服务器密码')
        self.input_Text(self.node_host_input, host, mark='输入服务器ip')
        self.clean_Text(self.node_p2pport_input)
        self.input_Text(self.node_p2pport_input, p2pport, mark='p2p port')
        self.upload_file(self.genesis_file, genesis_file)
        self.input_Text(self.node_script_input, script, mark='服务器文件路径')
        self.input_Text(self.server_user_input, user, mark='服务器用户名')
        self.click_Element(self.submit_btn, mark='提交')
        # time.sleep(30)  # 初始化节点

    def select_node_index(self):
        self.click_Element(self.nodeManger, mark='选择节点管理页卡')

    def edit_rpc_port(self, rpc, index=0):
        """
        编辑节点rpc端口，默认第一个
        """
        self.select_node_index()
        node_list = self.find_Elements(self.edit_btn)
        node_list[index].click()
        self.clean_Text(self.node_rpc_input)
        self.input_Text(self.node_rpc_input, rpc)
        self.click_Element(self.edit_submit_btn)

    def edit_normalnd_ip(self, ip, index=1):
        """
        修改观察者节点ip
        """
        self.select_node_index()
        node_list = self.find_Elements(self.edit_btn)
        node_list[index].click()
        self.clean_Text(self.node_host_input)
        self.input_Text(self.node_host_input, ip)
        self.click_Element(self.edit_submit_btn)

    def edit_normalnd_port(self, port, p2pport, index=1):
        """
        修改观察者节点ip
        """
        self.select_node_index()
        node_list = self.find_Elements(self.edit_btn)
        node_list[index].click()
        self.clean_Text(self.node_rpc_input)
        self.input_Text(self.node_rpc_input, port)
        self.clean_Text(self.node_p2pport_input)
        self.input_Text(self.node_p2pport_input, p2pport)
        self.click_Element(self.edit_submit_btn)

    def to_publicnd(self, index=0):
        """
        修改观察者节点为共识节点
        """
        self.select_node_index()
        node_list = self.find_Elements(self.edit_public_btn)
        node_list[index].click()
        self.click_Text('确 认')

    def to_normalnd(self, index=0):
        """
        修改共识节点为观察者节点
        """
        self.select_node_index()
        node_list = self.find_Elements(self.edit_normal_btn)
        node_list[index].click()
        self.click_Text('确 认')

    def stop_node(self, index=0):
        """
        禁用节点
        """

        self.select_node_index()
        node_list = self.find_Elements(self.stop_btn)
        node_list[index].click()
        self.click_Text('确 认')

    def delete_node(self, index=0):
        """
        删除节点
        """

        self.select_node_index()
        node_list = self.find_Elements(self.delete_btn)
        node_list[index].click()
        self.click_Text('确 认')

    def start_node(self, index=0):
        """
        启动节点
        """
        self.select_node_index()
        node_list = self.find_Elements(self.start_btn)
        node_list[index].click()
        self.click_Text('确 认')
import os
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
    stop_btn = (By.XPATH, '//*[text()="禁用"]')
    delete_btn = (By.XPATH, '//*[text()="删除"]')

    nodeManger = (By.XPATH, '//*[text()="节点管理"]')

    def add_node(self, name, desc, rpc, license_file, ip, pwd, host, p2pport, genesis_file, script, user,
                 docker=False):
        """
        添加节点的数据
        """
        self.select_node_index()
        self.click_Element(self.add_node)
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
        self.click_Element(self.license_file, mark='上传license')
        path = os.path.abspath('../..') + '\\uploadjson.exe'  # 上传文件
        os.system(fr'{path} {license_file}')
        time.sleep(2)
        self.input_Text(self.server_ip_input, ip, mark='输入服务器ip')
        self.input_Text(self.server_pwd_input, pwd, mark='输入服务器密码')
        self.input_Text(self.node_host_input, host, mark='输入服务器ip')
        self.clean_Text(self.node_p2pport_input)
        self.input_Text(self.node_p2pport_input, p2pport, mark='p2p port')
        self.click_Element(self.genesis_file)
        os.system(fr'{path} {genesis_file}')
        time.sleep(2)
        self.input_Text(self.node_script_input, script, mark='服务器文件路径')
        self.input_Text(self.server_user_input, user, mark='服务器用户名')
        self.click_Element(self.submit_btn, mark='提交')
        time.sleep(10)

    def select_node_index(self):
        self.click_Element(self.nodeManger,mark='选择节点管理页卡')

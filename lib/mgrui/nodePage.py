import os, time
from .basePage import BasePage
from .locator.nodemanger import NodeMangerLocator as loc


class NodePage(BasePage):

    def add_node(self, name, desc, rpc, license_file, ip, pwd, host, p2pport, genesis_file, script, user,
                 docker=False, ):
        self.click_Element(loc.add_node)
        self.input_Text(loc.node_name, name, mark='输入节点名称')
        self.input_Text(loc.node_desc, desc, mark='节点说明')
        self.input_Text(loc.node_rpc, rpc, mark='rpc端口')
        if docker:
            pass
        else:
            self.click_Element(loc.docker_choice)
            self.click_Text(docker)
        self.click_Element(loc.license, mark='上传license')
        path = os.path.abspath('..') + '\\uploadjson.exe'  # 上传文件
        os.system(fr'{path} {license_file}')
        time.sleep(2)
        self.input_Text(loc.server_ip, ip, mark='输入服务器ip')
        self.input_Text(loc.server_pwd, pwd, mark='输入服务器密码')
        self.click_Element(loc.node_type, mark='选择节点类型')
        self.click_Text(text='', mark='选择节点类型')
        self.input_Text(loc.node_host, host, mark='输入服务器ip')
        self.input_Text(loc.node_p2pport, p2pport, mark='p2p port')
        self.click_Element(loc.genesis_file)
        os.system(fr'{path} {genesis_file}')
        time.sleep(2)
        self.input_Text(loc.node_script, script, mark='服务器文件路径')
        self.input_Text(loc.server_user, user, mark='服务器用户名')
        self.click_Element(loc.submit, mark='提交')
        time.sleep(5)

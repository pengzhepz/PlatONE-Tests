from dataclasses import dataclass

from dacite import from_dict
from ruamel import yaml

from common.connectServer import connect_linux
from lib.env.node import NodeGroup, Infos
from lib.mgrapi import initChain, createNode
from setting import *


@dataclass
class Env(Infos):
    init: NodeGroup = None
    normal: NodeGroup = None

    def __post_init__(self):
        self.members = self.init.members + self.normal.members
        for member in self.members:
            self._fill_common_info(member)
            member.connect()
        self.__check_nodes()
        # if os.path.isabs(deploy_path):
        #     self.remote_node_path = "{}/{}".format(deploy_path, member.p2p_port)
        # else:
        #     self.remote_node_path = "{}/{}/{}".format(self.pwd, self.cfg.deploy_path, self.node_name)

    def __check_nodes(self):
        # todo: check the node info is not duplicated
        pass

    def running(self):
        running_list = []
        for member in self.members:
            p_id = \
                member.run_ssh("ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)[
                    0]
            if len(p_id) != 0:
                running_dict = {'host': member.host, 'pid': p_id.strip()}
                running_list.append(running_dict)
        return running_list

    def init_chain(self):
        pass

    def deploy(self):
        for member in self.members:
            p_id = member.run_ssh(
                "ps -ef|grep platone|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
            if len(p_id) != 0:
                print(p_id[0].strip())
                member.run_ssh("sudo -S -p '' kill -9 {}".format(int(p_id[0].strip())), member.password)
                logger.info("sotp node {} {}".format(member.host, member.p2p_port))
            path = deploy_path + "/node-" + str(member.p2p_port)
            member.run_ssh("sudo -S -p '' rm -rf {};mkdir -p {}".format(path, path), member.password)
            logger.info("mkdir {} success".format("/node-" + str(member.p2p_port)))
            member.run_ssh("cd {};wget {}".format(path, download_url + "linux.tar.gz"))
            logger.info("download {} success".format("/node-" + str(member.p2p_port)))
            member.run_ssh("cd {};tar -zxvf {}".format(path, "linux.tar.gz"))
            logger.info("decompression {} success".format("/node-" + str(member.p2p_port)))

        initChain.init_chain('platone-license', PLATONE_LICENSE_FILE, "liuxing", self.members[0].host, 1,
                             self.members[0].host, 'liuxing', self.members[0].p2p_port, self.members[0].password,
                             self.members[0].rpc_port,
                             '~/platone_test/node-16789/linux/scripts', 2, 1, 'platon',
                             'lax17sfqr79fzq6qgx3x9wv8259mjjjstjfhjyue4p')
        env.upload_genesis()
        for member in self.members[1:]:
            scripts_path = "~/" + deploy_path + "/node-" + str(member.p2p_port) + "/linux/scripts"
            createNode.create_node(genesis_filename='genesis.json', genesis_filepath=GENESIS_FILE,
                                   license_filename='platone-license', license_filepath=PLATONE_LICENSE_FILE,
                                   ip=member.host, nodeIp=member.host, nodeName="节点：" + member.host,
                                   p2pPort=member.p2p_port, password=member.password, rpcPort=member.rpc_port,
                                   scriptPath=scripts_path, userName=member.username,
                                   chain_rpc='http://'+self.members[0].host+':'+str(self.members[0].rpc_port),
                                   chain_address='lax17sfqr79fzq6qgx3x9wv8259mjjjstjfhjyue4p',
                                   privatekey='dfe074dc29a259f23c4dbca369faee16a82528af2324ef230811db89a704e8b6')

    def upload_genesis(self):
        if not os.path.exists(TMP_GENESIS):
            os.makedirs(TMP_GENESIS)
        if os.path.exists(TMP_GENESIS + "\genesis.json"):
            os.remove(TMP_GENESIS + "\genesis.json")
        ssh, sftp, t = connect_linux(self.members[0].host, self.members[0].username, self.members[0].password,
                                     self.members[0].ssh_port)
        conf_path = deploy_path + "/node-" + str(self.members[0].p2p_port) + "/linux/conf/"

        sftp.get(f'{conf_path}/genesis.json', r"{}\genesis.json".format(TMP_GENESIS))

        # for member in self.members[1:]:
        #     ssh, sftp, t = connect_linux(member.host, member.username, member.password, member.ssh_port)
        #     remote_genesis = deploy_path + "/node-" + str(member.p2p_port) + "/linux/conf/genesis.json"
        #     sftp.put(TMP_GENESIS, remote_genesis)

    def start(self):
        for member in self.members[1:]:
            scripts_path = deploy_path + "~/node-" + str(member.p2p_port) + "/linux/scripts_path/scripts"
            # createNode.create_node('genesis.json', GENESIS_FILE, 'platone-license',
            #                        PLATONE_LICENSE_FILE,
            #                        "服务器地址：" + member.host, member.host, 1, member.host, "节点：" + member.host,
            #                        member.p2p_port,
            #                        member.username, member.password, member.rpc_port, scripts_path, 2, 1)
            print('genesis.json', GENESIS_FILE, 'platone-license',
                  PLATONE_LICENSE_FILE,
                  "服务器地址：" + member.host, member.host, 1, member.host, "节点：" + member.host,
                  member.p2p_port,
                  member.username, member.password, member.rpc_port, scripts_path, 2, 1)

    def all_stop(self):
        for member in self.members:
            p_id = member.run_ssh(
                "ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
            if len(p_id) != 0:
                print("sudo kill -9 {}".format(int(p_id[0].strip())))
                member.run_ssh("sudo kill -9 {}".format(int(p_id[0].strip())), member.password)
                logger.info("sotp node {} {}".format(member.host, member.p2p_port))

    # def restart():
    #     pass

    def clean(self):
        env.all_stop()
        for member in self.members:
            path = deploy_path + "/node-" + str(member.p2p_port)
            member.run_ssh("sudo -S -p '' rm -rf {}".format(path), member.password)
            logger.info("clean {} success".format("/node-" + str(member.p2p_port)))


# create env obj
def env_factory(nodes_file) -> Env:
    with open(nodes_file, encoding='utf-8') as f:
        nodes_dict = yaml.load(f, Loader=yaml.Loader)
    return from_dict(Env, nodes_dict)


if __name__ == '__main__':
    env = env_factory('nodes_template.yml')
    # print(env.members)
    # print(env.running())
    # env.all_stop()
    # env.clean()
    env.deploy()
    # env.upload_genesis()
    # env.start()
    # env.upload_genesis()

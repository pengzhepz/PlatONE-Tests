import random


from lib.env.client import Client
from lib.env.node import Infos, NodeGroup
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from dataclasses import dataclass
from typing import List

from dacite import from_dict
from ruamel import yaml

from common.connectServer import connect_linux, wait_connect_web3
from common.getYaml import LoadFile
from common.key import *

from lib.mgrapi import initChain, createNode
from setting import *
from platone import admin



@dataclass
class Env(Infos):
    init: NodeGroup = None
    normal: NodeGroup = None

    def __post_init__(self):
        self.members = self.init.members + self.normal.members
        for member in self.members:
            self._fill_common_info(member)
            member.connect()
            self.url = "http://{}:{}".format(member.host, member.rpc_port)
        self.__check_nodes()


        self.max_worker = 30
    #
        # Client obj list
        self.__consensus_client_list = []
        self.__normal_client_list = []





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
                "ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
            if len(p_id) != 0:
                print(p_id[0].strip())
                member.run_ssh("sudo -S -p '' kill -9 {}".format(int(p_id[0].strip())), member.password)
                logger.info("sotp node {} {}".format(member.host, member.p2p_port))

            #更新Linux包：
            # path = deploy_path + "/node-" + str(member.p2p_port)
            # member.run_ssh("sudo -S -p '' rm -rf {};mkdir -p {}".format(path, path), member.password)
            # logger.info("mkdir {} success".format("/node-" + str(member.p2p_port)))
            # member.run_ssh("cd {};wget {}".format(path, download_url + "linux.tar.gz"))
            # logger.info("download {} success".format("/node-" + str(member.p2p_port)))
            # member.run_ssh("cd {};tar -zxvf {}".format(path, "linux.tar.gz"))
            # logger.info("decompression {} success".format("/node-" + str(member.p2p_port)))

            #只更新二进制包：
            path = deploy_path + "/node-" + str(member.p2p_port) + "/linux/bin/platone"
            member.run_ssh("sudo -S -p '' rm -rf {}".format(path), member.password)
            logger.info("remove {} success".format(path))

            remove_path = deploy_path + "/node-" + str(member.p2p_port) + "/linux"
            member.run_ssh("cd {};sudo -S -p '' rm -rf {}".format(remove_path, "data/ conf/genesis.json platone-license"), member.password)
            logger.info("Clear {} success".format("cache"))

            cd_path = deploy_path + "/node-" + str(member.p2p_port) + "/linux/bin/"
            member.run_ssh("cd {};wget {}".format(cd_path, download_url + "platone"))
            logger.info("download {} success".format("platone"))

            member.run_ssh("cd {};chmod u+x {}".format(cd_path, "platone"))
            logger.info("Authorization succeeded ")


        script_path = "~/" + deploy_path + "/node-" + str(self.init.p2p_port) + "/linux/scripts"
        initChain.init_chain('platone-license', PLATONE_LICENSE_FILE, "liuxing", self.members[0].host, 1,
                             self.members[0].host, 'liuxing', self.members[0].p2p_port, self.members[0].password,
                             self.members[0].rpc_port,
                             script_path, 2, 1, self.members[0].username,
                             'lax17sfqr79fzq6qgx3x9wv8259mjjjstjfhjyue4p')
        self.upload_genesis()
        for member in self.members[1:]:
            scripts_path = "~/" + deploy_path + "/node-" + str(member.p2p_port) + "/linux/scripts"
            createNode.create_node(genesis_filename='genesis.json', genesis_filepath=GENESIS_FILE,
                                   license_filename='platone-license', license_filepath=PLATONE_LICENSE_FILE,
                                   ip=member.host, nodeIp=member.host, nodeName="节点：" + str(member.host) + ":" + str(member.rpc_port),
                                   p2pPort=member.p2p_port, password=member.password, rpcPort=member.rpc_port,
                                   scriptPath=scripts_path, userName=member.username,
                                   chain_rpc='http://'+self.members[0].host+':'+str(self.members[0].rpc_port),
                                   chain_address='lax17sfqr79fzq6qgx3x9wv8259mjjjstjfhjyue4p',
                                   privatekey='dfe074dc29a259f23c4dbca369faee16a82528af2324ef230811db89a704e8b6')

        self.__rewrite_node_file()
        # self.parse_client()



    def parse_client(self):

        def init(node_config):
            return Client(node_config)

        logger.info("parse node to node object")
        with ThreadPoolExecutor(max_workers=self.max_worker) as executor:
            futures = [executor.submit(init, pair) for pair in self.consensus_node_config_list]
            done, unfinished = wait(futures, timeout=30, return_when=ALL_COMPLETED)
        for do in done:
            self.__consensus_client_list.append(do.result())

        if self.noconsensus_node_config_list:
            with ThreadPoolExecutor(max_workers=self.max_worker) as executor:
                futures = [executor.submit(init, pair) for pair in self.noconsensus_node_config_list]

                done, unfinished = wait(futures, timeout=30, return_when=ALL_COMPLETED)
            for do in done:
                self.__normal_client_list.append(do.result())





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


    def clean(self, env):
        env.all_stop()
        for member in self.members:
            path = deploy_path + "/node-" + str(member.p2p_port)
            member.run_ssh("sudo -S -p '' rm -rf {}".format(path), member.password)
            logger.info("clean {} success".format("/node-" + str(member.p2p_port)))



    def  stop_designated_node(self, rpc):
        for member in self.members:
            if str(member.host) + ':' + str(member.rpc_port) == rpc[7:]:
                p_id = member.run_ssh(
                    "ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
                member.run_ssh("sudo -S -p '' kill -9 {}".format(int(p_id[0].strip())), member.password)
                logger.info("sotp node {} {}".format(member.host, member.p2p_port))



    def clean_designated_node(self, rpc, ledger_name):
        for member in self.members:
            if str(member.host) + ':' + str(member.rpc_port) == rpc[7:]:
                print(str(member.host) + ':' + str(member.rpc_port))
                p_id = member.run_ssh(
                    "ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
                print("sudo kill -9 {}".format(int(p_id[0].strip())))
                member.run_ssh("sudo -S -p '' kill -9 {}".format(int(p_id[0].strip())), member.password)
                logger.info("sotp node {} {}".format(member.host, member.p2p_port))
                path = "~/" + deploy_path + "/node-" + str(member.p2p_port) + "/linux/data/node-1/platone/"
                remove_file = ledger_name
                member.run_ssh("cd {};sudo -S -p '' rm -rf {}".format(path, remove_file), member.password)
                logger.info("clean {} success".format(remove_file))
                # member.run_ssh()
                break
        else:
            assert 1 == 2, 'Rpc does not exist '

    def clean_subledger(self, rpc, ledger_name):
        for member in self.members:
            if str(member.host) + ':' + str(member.rpc_port) == rpc[7:]:
                print(str(member.host) + ':' + str(member.rpc_port))
                # p_id = member.run_ssh(
                #     "ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
                # print("sudo kill -9 {}".format(int(p_id[0].strip())))
                # member.run_ssh("sudo -S -p '' kill -9 {}".format(int(p_id[0].strip())), member.password)
                # logger.info("sotp node {} {}".format(member.host, member.p2p_port))
                path = "~/" + deploy_path + "/node-" + str(member.p2p_port) + "/linux/data/node-1/platone/"
                remove_file = ledger_name
                member.run_ssh("cd {};sudo -S -p '' rm -rf {}".format(path, remove_file), member.password)
                logger.info("clean {} success".format(remove_file))
                # member.run_ssh()
                break
        else:
            assert 1 == 2, 'Rpc does not exist '



    def start_designated_node(self, rpc):
        for member in self.members:
            if str(member.host) + ':' + str(member.rpc_port) == rpc[7:]:
                scripts_path = "~/" + deploy_path + "/node-" + str(member.p2p_port) + "/linux/scripts"
                member.run_ssh("cd {};sudo -S -p '' ./start-node.sh".format(scripts_path), member.password)
                logger.info("Start {} success",format(rpc))
                p_id = member.run_ssh(
                    "ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
                assert isinstance(p_id, list)




    def __fill_consensus_node_config(self, node_config: dict):
        if not node_config.get("username"):
            self.__is_update_node_file = True
            node_config["username"] = 'juzix'
        if not node_config.get("password"):
            self.__is_update_node_file = True
            node_config["password"] = '123456'
        if not node_config.get("ssh_port"):
            self.__is_update_node_file = True
            node_config["ssh_port"] = 22
        if not node_config.get("p2p_port"):
            self.__is_update_node_file = True
            node_config["p2p_port"] = 17789
        if not node_config.get("rpc_port"):
            self.__is_update_node_file = True
            node_config["rpc_port"] = 7789
        if not node_config.get("url"):
            self.__is_update_node_file = True
            node_config["url"] = "http://{}:{}".format(node_config["host"], node_config["rpc_port"])
            self.__rpc = wait_connect_web3(node_config["url"])
            self.__is_connected = True
            self.admin = admin.Admin(self.__rpc)
            self.node_info = self.admin.nodeInfo
            self.node_id = self.node_info["id"]
            self.node_pubkey = self.node_info["blsPubKey"]
        if not node_config.get("node_id"):
            self.__is_update_node_file = True
            node_config["node_id"] = self.node_id
        if not node_config.get("node_pubkey"):
            self.__is_update_node_file = True
            node_config["node_pubkey"] = self.node_pubkey
        # if node_config.get("wsport"):
        #     self.__is_update_node_file = True
        #     node_config["wsurl"] = "ws://{}:{}".format(node_config["host"], node_config["wsport"])
        return node_config



    def __fill_noconsensus_node_config(self, node_config: dict):
        if not node_config.get("username"):
            self.__is_update_node_file = True
            node_config["username"] = 'juzix'
        if not node_config.get("password"):
            self.__is_update_node_file = True
            node_config["password"] = '123456'
        if not node_config.get("ssh_port"):
            self.__is_update_node_file = True
            node_config["ssh_port"] = 22
        if not node_config.get("p2p_port"):
            self.__is_update_node_file = True
            node_config["p2p_port"] = 17790
        if not node_config.get("rpc_port"):
            self.__is_update_node_file = True
            node_config["rpc_port"] = 7790
        if not node_config.get("url"):
            self.__is_update_node_file = True
            node_config["url"] = "http://{}:{}".format(node_config["host"], node_config["rpc_port"])
            self.__rpc = wait_connect_web3(node_config["url"])
            self.__is_connected = True
            self.admin = admin.Admin(self.__rpc)
            self.node_info = self.admin.nodeInfo
            self.node_id = self.node_info["id"]
            self.node_pubkey = self.node_info["blsPubKey"]
        if not node_config.get("node_id"):
            self.__is_update_node_file = True
            node_config["node_id"] = self.node_id
        if not node_config.get("node_pubkey"):
            self.__is_update_node_file = True
            node_config["node_pubkey"] = self.node_pubkey
        # if node_config.get("wsport"):
        #     self.__is_update_node_file = True
        #     node_config["wsurl"] = "ws://{}:{}".format(node_config["host"], node_config["wsport"])
        return node_config


    def __rewrite_node_file(self):
        logger.info("rewrite node file")
        __is_update_node_file = False
        self.node_config = LoadFile(NODES_FILE).get_data()
        self.consensus_node_config_list = self.node_config.get("init").get("members", [])
        self.noconsensus_node_config_list = self.node_config.get("normal").get("members", [])
        self.node_config_list = self.consensus_node_config_list + self.noconsensus_node_config_list

        result, result_consensus_list, result_noconsensus_list = {}, [], []
        if len(self.consensus_node_config_list) >= 1:
            for node_config in self.consensus_node_config_list:
                result_consensus_list.append(self.__fill_consensus_node_config(node_config))
            result["consensus"] = result_consensus_list
        if self.noconsensus_node_config_list and len(self.noconsensus_node_config_list) >= 1:
            for node_config in self.noconsensus_node_config_list:
                result_noconsensus_list.append(self.__fill_noconsensus_node_config(node_config))
            result["noconsensus"] = result_noconsensus_list
        if self.__is_update_node_file:
            self.consensus_node_config_list = result_consensus_list
            self.noconsensus_node_config_list = result_noconsensus_list
            with open(NIDE_INFO_FILE, encoding="utf-8", mode="w") as f:
                yaml.dump(result, f, Dumper=yaml.RoundTripDumper)

    def get_node_file(self):
        logger.info("rewrite node file")
        __is_update_node_file = False
        self.nodes_info = LoadFile(NIDE_INFO_FILE).get_data()
        self.consensus_node_config_list = self.nodes_info.get("consensus", [])
        self.noconsensus_node_config_list = self.nodes_info.get("noconsensus", [])
        self.node_config_list = self.consensus_node_config_list + self.noconsensus_node_config_list



    # @property
    def consensus_client_list(self) -> List[Client]:
        return self.__consensus_client_list

    # @property
    def normal_client_list(self) -> List[Client]:
        return self.__normal_client_list



    def get_all_clients(self) -> List[Client]:
        """
        Get all client objects
        :return: Client object
        """
        return self.__consensus_client_list + self.__normal_client_list


    def get_consensus_client_by_index(self, index) -> Client:
        """
        Get a consensus client based on the index
        :param index:
        :return: Client object
        """
        return self.__consensus_client_list[index]


    def get_normal_client_by_index(self, index) -> Client:
        """
        Get a normal client based on the index
        :param index:
        :return: Client object
        """
        return self.__normal_client_list[index]

    def get_a_normal_client(self) -> Client:
        """
        Get the first normal client
        :return: Client object
        """
        return self.__normal_client_list[0]

    def get_a_consensus_client(self) -> Client:
        """
        Get the first normal client
        :return: Client object
        """
        return self.__consensus_client_list[0]


    def get_rand_client(self) -> Client:
        """
        Randomly obtain a consensus client
        :return: Client object
        """
        print('kanxia', self.consensus_client_list)
        return random.choice(self.consensus_client_list)








# create env obj
def env_factory(nodes_file) -> Env:
    with open(nodes_file, encoding='utf-8') as f:
        nodes_dict = yaml.load(f, Loader=yaml.Loader)
    return from_dict(Env, nodes_dict)


if __name__ == '__main__':
    pass
    # env = env_factory('nodes_template.yml')
    # # print(env.members)
    # # print(env.running())
    # # env.all_stop()
    # # env.clean()
    # env.deploy()
    # # env.upload_genesis()
    # env.start()
    # env.upload_genesis()
    # print(env.members)
    # env.write_filexxx()


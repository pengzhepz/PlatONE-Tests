from dataclasses import dataclass

from dacite import from_dict
from ruamel import yaml

from lib.env.node import NodeGroup, Infos
from lib.mgrapi import initChain
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
            member.run_ssh("ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)[0]
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
                member.run_ssh("sudo kill -9 %s" % p_id[0].strip(), member.password)
                logger.info("sotp node {} {}".format(member.host, member.p2p_port))
            path = deploy_path + "/node-" + str(member.p2p_port)
            member.run_ssh("sudo -S -p '' rm -rf {};mkdir -p {}".format(path, path), member.password)
            logger.info("mkdir {} success".format("/node-" + str(member.p2p_port)))
            member.run_ssh("cd {};wget {}".format(path, download_url + "linux.tar.gz"))
            logger.info("download {} success".format("/node-" + str(member.p2p_port)))
            member.run_ssh("cd {};tar -zxvf {}".format(path, "linux.tar.gz"))
            logger.info("decompression {} success".format("/node-" + str(member.p2p_port)))

        result = initChain.init_chain('license_filename', license_filepath, "liuxing", self.members[0].host, 1,
                             self.members[0].host, 'liuxing', self.members[0].p2p_port, self.members[0].password,
                             self.members[0].rpc_port,
                             scripts_path, 2, 1, 'test', 'lax17nqy9qdphfmz3fj598rq59zek4t7hzatju8mn6')
        print(result)

    def start(self):
        print(license_filepath)

    def all_stop(self):
        for member in self.members:
            p_id = member.run_ssh(
                "ps -ef|grep platon|grep port|grep %s|grep -v grep|awk {'print $2'}" % member.p2p_port)
            if len(p_id) != 0:
                member.run_ssh("sudo kill -9 %s" % p_id[0].strip(), member.password)
                logger.info("sotp node {} {}".format(member.host, member.p2p_port))

    def restart(self):
        pass

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
    # env.start()

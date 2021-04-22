from dataclasses import dataclass, field
from typing import List
from dacite import from_dict
from ruamel import yaml

from lib.env.node import Node, NodeGroup


@dataclass
class Env(Node):
    init: NodeGroup = None
    normal: NodeGroup = None

    def __post_init__(self):
        members = self.init.members + self.normal.members
        for member in members:
            self._fill_common_info(member)
        self.__check_nodes()

    def __check_nodes(self):
        # todo: check the node info is not duplicated
        pass

    def running(self):
        pass

    def deploy(self):
        print('deployed!')

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def clean(self):
        pass


# create env obj
def env_factory(nodes_file) -> Env:
    with open(nodes_file, encoding='utf-8') as f:
        nodes_dict = yaml.load(f, Loader=yaml.Loader)
    return from_dict(Env, nodes_dict)


if __name__ == '__main__':
    env = env_factory('nodes_template.yml')
    env.deploy()

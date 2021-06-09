from dataclasses import dataclass, asdict, field
from typing import List

import yaml
from dacite import from_dict
from lib.env.host import Host


@dataclass
class Infos:
    username: str = None
    password: str = None
    ssh_port: int = 22
    p2p_port: int = None
    rpc_port: int = None
    ws_port: int = None

    def _fill_common_info(self, node):
        info_dict = asdict(self)
        for k, v in info_dict.items():
            if not v:
                continue
            if hasattr(node, k) and not getattr(node, k):
                setattr(node, k, v)


@dataclass
class Node(Host):
    p2p_port: int = None
    rpc_port: int = None
    ws_port: int = None

    def to_dict(self):
        return asdict(self)


@dataclass
class NodeGroup(Infos):
    members: List[Node] = field(default_factory=[])

    def __post_init__(self):
        for member in self.members:
            self._fill_common_info(member)



#
def node_factory(nodes_file) -> Node:
    with open(nodes_file, encoding='utf-8') as f:
        nodes_dict = yaml.load(f, Loader=yaml.Loader)
    return from_dict(Node, nodes_dict)
#
#
#
# if __name__ == '__main__':
    # node = node_factory('nodes_template.yml')
    # print(node.rpc_port)
    # info =  Infos()
    # print(info.rpc_port)
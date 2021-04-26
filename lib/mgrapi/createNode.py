import requests
from setting import mgrapi_host


def create_node(genesis_filename, genesis_filepath, license_filename, license_filepath, desc, ip, nodeId, nodeIp,
                nodeName, p2pPort, userName, password, rpcPort, scriptPath, useDocker, smFlg):
    """
    创建节点
    :param genesis_filename: 创世文件名字
    :param genesis_filepath: 创世文件路径
    :param license_filename: 证书文件名
    :param license_filepath: 证书文件路径
    :param desc: 节点描述
    :param ip: 服务器ip
    :param nodeId: 节点id
    :param nodeIp: 节点ip
    :param nodeName: 节点名字
    :param p2pPort: 节点p2p端口
    :param userName: 登录服务器用户
    :param password: 登录服务器密码
    :param rpcPort: 节点rpc端口
    :param scriptPath: platone管理工具执行目录,如果使用docker启动此参数可以不输入
    :param useDocker: 是否使用docker部署:1-是，2-否
    :param smFlg: 是否使用国密:1-是，2-否
    :return:
    """
    file = {'genesis': (genesis_filename, open(genesis_filepath, 'rb'), 'application/json'),
            'platoneLicense': (
                license_filename, open(license_filepath, 'rb'),
                'application/octet-stream'),
            'desc': (None, desc), 'ip': (None, ip),
            'nodeId': (None, nodeId), 'nodeIp': (None, nodeIp),
            'nodeName': (None, nodeName),
            'p2pPort': (None, p2pPort), 'password': (None, userName),
            'rpcPort': (None, password),
            'scriptPath': (None, rpcPort), 'useDocker': (None, scriptPath),
            'smFlg': (None, useDocker),
            'userName': (None, smFlg)}

    res = requests.post(mgrapi_host + '/proxyApi/proxy/addNode', files=file)
    return res

import requests
from setting import mgrapi_host


def init_chain(license_filename, license_filepath, desc, ip, nodeId, nodeIp, nodeName, p2pPort, password, rpcPort,
               scriptPath, useDocker, smFlg, userName, creatorAddress):
    """

    :param license_filename: license文件的名字
    :param license_filepath: license文件的路径
    :param desc: 链的描述
    :param ip: 服务器ip
    :param nodeId: 节点id
    :param nodeIp: 节点ip
    :param nodeName: 节点名字
    :param p2pPort: 节点p2p端口
    :param password: 服务器登录密码
    :param rpcPort: 节点rpc端口
    :param scriptPath: platone管理工具执行目录,如果使用docker启动此参数可以不输入
    :param useDocker: 是否使用docker部署:1-是，2-否
    :param smFlg: 是否使用国密:1-是，2-否
    :param userName: 服务器登录用户
    :param creatorAddress: 链创建者地址
    :return:
    """
    file = {'platoneLicense': (license_filename, open(license_filepath, 'rb'), 'application/octet-stream'),
            'desc': (None, desc), 'ip': (None, ip),
            'nodeId': (None, nodeId), 'nodeIp': (None, nodeIp), 'nodeName': (None, nodeName),
            'p2pPort': (None, p2pPort), 'password': (None, password),
            'rpcPort': (None, rpcPort),
            'scriptPath': (None, scriptPath), 'useDocker': (None, useDocker),
            'smFlg': (None, smFlg),
            'userName': (None, userName), 'creatorAddress': (None, creatorAddress)}

    res = requests.post(mgrapi_host + '/proxyApi/proxy/initChain', files=file)
    return res

import requests
from setting import mgrapi_host
from platone.node import Node
from platone import HTTPProvider, Web3


def create_node(genesis_filename, genesis_filepath, license_filename, license_filepath, ip, nodeIp,
                nodeName, p2pPort, userName, password, rpcPort, scriptPath, chain_rpc, chain_address,
                privatekey, chain_id=200, nodeId=1, smFlg=1, useDocker=2, desc='desc'):
    """
    创建节点,并加入到链中
    :param genesis_filename: 创世文件名字
    :param genesis_filepath: 创世文件路径
    :param license_filename: 证书文件名
    :param license_filepath: 证书文件路径
    :param desc: 节点描述
    :param ip: 服务器ip
    :param nodeId: 节点id，默认1
    :param nodeIp: 节点ip
    :param nodeName: 节点名字，必须唯一不能重复
    :param p2pPort: 节点p2p端口
    :param userName: 登录服务器用户
    :param password: 登录服务器密码
    :param rpcPort: 节点rpc端口
    :param scriptPath: platone管理工具执行目录,如果使用docker启动此参数可以不输入
    :param useDocker: 是否使用docker部署:1-是，2-否，默认2
    :param smFlg: 是否使用国密:1-是，2-否，默认1
    chain_rpc: 主链的节点信息
    chain_address: 节点拥有者地址
    privatekey: 主链创世地址的私钥
    :return:
    """
    print(f'========================》 第一步：启动节点《========================')
    file = {'genesis': (genesis_filename, open(genesis_filepath, 'rb'), 'application/json'),
            'platoneLicense': (
                license_filename, open(license_filepath, 'rb'),
                'application/octet-stream'),
            'desc': (None, desc), 'ip': (None, ip),
            'nodeId': (None, nodeId), 'nodeIp': (None, nodeIp),
            'nodeName': (None, nodeName),
            'p2pPort': (None, p2pPort), 'password': (None, password),
            'rpcPort': (None, rpcPort),
            'scriptPath': (None, scriptPath), 'useDocker': (None, useDocker),
            'smFlg': (None, smFlg),
            'userName': (None, userName)}

    res = requests.post(mgrapi_host + '/proxyApi/proxy/addNode', files=file).json()

    print(f'========================》 第二步：把子节点加入主链中《========================')
    web3 = Web3(HTTPProvider(chain_rpc), chain_id=chain_id, multi_ledger=True, encryption_mode='SM')
    res_msg = Node(web3).add(name=nodeName, owner=chain_address, desc=desc,
                             pubkey=res['data']['publicKey'],
                             bls_pubkey=res['data']['blsPubKey'],
                             host_address=ip, rpc_port=rpcPort, p2p_port=p2pPort,
                             private_key=privatekey,tx_cfg={})
    return res_msg


if __name__ == '__main__':
    r = create_node(genesis_filename='genesis.json', genesis_filepath=r'C:\Users\juzix\Documents\genesis.json',
                    license_filename='platone-license', license_filepath=r'C:\Users\juzix\Documents\platone-license',
                    desc='no', nodeId=1, nodeIp='192.168.120.136', nodeName='node-98', p2pPort=11443,
                    userName='juzix', password='123456', rpcPort=1443, scriptPath='~/linux/scripts', useDocker=2,
                    smFlg=1, ip='192.168.120.136', chain_rpc='http://192.168.120.133:7789',
                    chain_address='lax1sqhslzzw6gvff5awk3lk937hndkhdk6twke942',
                    privatekey='da2b4214817a9d04a53206bc9d2cf93e76f4cd799d33bcb9022bbe6b7d2aa693')
    print(r)

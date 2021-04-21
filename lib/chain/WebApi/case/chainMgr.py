import requests
from common.utils import get_test_data
from common.getConfig import get_env


def init_chain():
    """
    创建链，通过
    :return:
    """

    host = get_env('test', 'host')
    test_list = list(get_test_data('../data/genesisChain.yaml'))
    params = test_list[0]['paramters']
    # print(host, test_list[0]['path'], params)

    file = {'platoneLicense': (
        params['platoneLicense']['filename'], open(params['platoneLicense']['filepath'], 'rb'),
        'application/octet-stream'),
        'desc': (None, params['desc']), 'ip': (None, params['ip']),
        'nodeId': (None, params['nodeId']), 'nodeIp': (None, params['nodeIp']), 'nodeName': (None, params['nodeName']),
        'p2pPort': (None, params['p2pPort']), 'password': (None, params['password']),
        'rpcPort': (None, params['rpcPort']),
        'scriptPath': (None, params['scriptPath']), 'useDocker': (None, params['useDocker']),
        'smFlg': (None, params['smFlg']),
        'userName': (None, params['userName']), 'creatorAddress': (None, params['creatorAddress'])}

    res = requests.post(host + test_list[0]['path'], files=file)
    return res


if __name__ == '__main__':
    i = init_chain()
    print(i.status_code, i.text)
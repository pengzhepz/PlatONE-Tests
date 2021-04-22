import requests
from lib.chain.WebApi.common.getConfig import get_env
from lib.chain.WebApi.common.utils import get_test_data
from lib.chain.WebApi.data.host import host

# header = {'Content-Type': 'multipart/form-data'}
# header = {}
# cookies = "smFlg=1; role=ChainCreator; privateKey=ed06a5fa0780c70e2a644da981f29b95209ecb455c9c6755eaf6d970c12bf177; from=lax1vaeqh6zlcj6wgw6cs3ajxqj9ynwcz52gwus9rp; wallet={%22version%22:3%2C%22id%22:%22bdb942be-333a-4693-979b-4ef9b187b553%22%2C%22address%22:%22lax1vaeqh6zlcj6wgw6cs3ajxqj9ynwcz52gwus9rp%22%2C%22crypto%22:{%22ciphertext%22:%22a224b1f6930a15a5ae6c9bffe61ce7f621c1c19f7e1e741c666815c5a218787a%22%2C%22cipherparams%22:{%22iv%22:%220b8ea9bbbc7f0b61ca38628884f85be4%22}%2C%22cipher%22:%22aes-128-ctr%22%2C%22kdf%22:%22scrypt%22%2C%22kdfparams%22:{%22dklen%22:32%2C%22salt%22:%224855ea4be10ae5a479c073372521b6a251c0f087d1a6092a7989ec568aa57232%22%2C%22n%22:8192%2C%22r%22:8%2C%22p%22:1}%2C%22mac%22:%225d26ff52bdb1d4f09bd10ac385d40eb73966339ab98a3814f3322304e229958a%22}}; url=http://192.168.120.133:1331"
# header['Cookie'] = cookies

def create_node():
    """
    创建节点（在界面上找不到，开发回复：还要调合约的添加节点）
    :return:
    """

    test_list = list(get_test_data('../data/createNode.yaml'))
    params = test_list[0]['paramters']

    file = {'genesis': (params['genesis']['filename'], open(params['genesis']['filepath'], 'rb'), 'application/json'),
            'platoneLicense': (
                params['platoneLicense']['filename'], open(params['platoneLicense']['filepath'], 'rb'),
                'application/octet-stream'),
            'desc': (None, params['desc']), 'ip': (None, params['ip']),
            'nodeId': (None, params['nodeId']), 'nodeIp': (None, params['nodeIp']),
            'nodeName': (None, params['nodeName']),
            'p2pPort': (None, params['p2pPort']), 'password': (None, params['password']),
            'rpcPort': (None, params['rpcPort']),
            'scriptPath': (None, params['scriptPath']), 'useDocker': (None, params['useDocker']),
            'smFlg': (None, params['smFlg']),
            'userName': (None, params['userName'])}

    res = requests.post(host + test_list[0]['path'], files=file)
    return res

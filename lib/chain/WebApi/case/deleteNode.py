import requests
from lib.chain.WebApi.common.getConfig import get_env
from lib.chain.WebApi.common.utils import get_test_data
from lib.chain.WebApi.data.host import host


def delete_node():
    """
    清理节点，未通过（开发回复：暂未开放）
    :return:
    """

    test_list = list(get_test_data('../data/clearNode.yaml'))
    params = test_list[0]['paramters']
    # print(host,test_list[0]['path'],params)
    header = {'Content-Type': 'application/json'}

    res = requests.post(host + test_list[0]['path'], json=params, headers=header)
    return res

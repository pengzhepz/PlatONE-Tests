import requests
from common.utils import get_test_data
from common.getConfig import get_env


def delete_node():
    """
    清理节点，未通过（开发回复：暂未开放）
    :return:
    """

    host = get_env('test', 'host')
    test_list = list(get_test_data('../data/clearNode.yaml'))
    params = test_list[0]['paramters']
    # print(host,test_list[0]['path'],params)
    header = {'Content-Type': 'application/json'}

    res = requests.post(host + test_list[0]['path'], json=params, headers=header)
    return res

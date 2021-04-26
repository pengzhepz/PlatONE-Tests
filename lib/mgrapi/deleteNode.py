from setting import mgrapi_host
import requests


def delete_node(username, pwd, ip, scriptpath, usedocker=1):
    """
    清理节点（未测试通过，暂未对外开放）
    :param username: 服务器登录用户
    :param pwd: 服务器登录密码
    :param ip: 服务器ip
    :param scriptpath: 服务器文件路径
    :param usedocker: 是否docker部署：1-是，2-否
    :return:
    """

    header = {'Content-Type': 'application/json'}
    params = {'password': pwd, 'useDocker': usedocker, 'ip': ip, 'scriptPath': scriptpath,
              'userName': username}
    res = requests.post(mgrapi_host + '/proxyApi/proxy/clearNode', json=params, headers=header)
    return res

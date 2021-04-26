import requests
from setting import mgrapi_host


def download_json(filetype, ip, scriptpath, username, pwd, usedocker=1):
    """
    genesis.json文件下载,只能在主节点上操作
    :param filetype: 下载文件类型:1-genesis.json，2-static-nodes.json
    :param ip: 服务器ip
    :param scriptpath: 服务器文件路径
    :param username: 服务器登录用户
    :param pwd: 服务器登录密码
    :param usedocker: 是否docker部署：1-是，2-否
    :return:
    """

    header = {'Content-Type': 'application/json'}
    params = {'fileType': filetype, 'useDocker': usedocker, 'ip': ip, 'scriptPath': scriptpath, 'userName': username,
              'password': pwd}
    res = requests.post(mgrapi_host + '/proxyApi/proxy/genesisFileDownload', json=params, headers=header)
    return res

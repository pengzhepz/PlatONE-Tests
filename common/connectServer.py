import paramiko


def connect_linux(ip, user, pwd, port=22):
    """
    1.连接linux服务器
    2.command： 执行Linux命令
    """

    with paramiko.SSHClient() as ssh:
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=ip, port=port, username=user, password=pwd)
        # # 执行命令
        # stdin, stdout, stderr = ssh.exec_command(command)
        # # 获取命令结果
        # result = str(stdout.read(), encoding='utf-8')
        # print(result)
    return ssh

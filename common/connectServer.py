import paramiko
from loguru import logger


def connect_linux(ip, username, password, port=22):
    """
     Use the account password to connect to the linux server
     :param ip: server ip
     :param username: username
     :param password: password
     :param port:
     :return:
         ssh:Ssh instance for executing the command ssh.exec_command(cmd)
         sftp:File transfer instance for uploading and downloading files sftp.get(a,b)Download a to b, sftp.put(a,b) upload a to b
         t:Connection instance for closing the connection t.close()
     """
    t = paramiko.Transport((ip, port))
    t.connect(username=username, password=password)
    ssh = paramiko.SSHClient()
    ssh._transport = t
    sftp = paramiko.SFTPClient.from_transport(t)
    return ssh, sftp, t


def run_ssh(ssh, cmd, password=None):
    try:
        stdin, stdout, _ = ssh.exec_command("source /etc/profile;%s" % cmd)
        if password:
            stdin.write(password + "\n")
        stdout_list = stdout.readlines()
        # if len(stdout_list):
        # log.debug('{}:{}'.format(cmd, stdout_list))
    except Exception as e:
        raise e
    return stdout_list


def run_ssh_cmd(ssh, cmd, password=None, password2=None, password3=None):
    try:
        logger.info('execute shell cmd::: {} '.format(cmd))
        stdin, stdout, _ = ssh.exec_command("source /etc/profile;%s" % cmd)
        if password:
            stdin.write(password + "\n")
        if password2:
            stdin.write(password2 + "\n")
        if password3:
            stdin.write(password3 + "\n")

        stdout_list = stdout.readlines()
        # if len(stdout_list):
        #     log.info('{}:{}'.format(cmd, stdout_list))
    except Exception as e:
        raise e
    return stdout_list

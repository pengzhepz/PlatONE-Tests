from dataclasses import dataclass

import paramiko
from paramiko import SSHException

from common.connectServer import connect_linux


@dataclass
class Host:
    host: str = None
    username: str = None
    password: str = None
    ssh_port: int = 22
    sftp = None
    ssh = None

    def connect(self):
        self.ssh, self.sftp, _ = connect_linux(self.host, self.username, self.password, self.ssh_port)

    def run_ssh(self, cmd, password=None):
        stdin, stdout, _ = self.ssh.exec_command("source /etc/profile;%s" % cmd)
        if password:
            stdin.write(password + "\n")
        return stdout.readlines()

    def pwd(self):
        pwd_list = self.run_ssh("pwd")
        pwd = pwd_list[0].strip("\r\n")
        return pwd

    def root_run_ssh(self, cmd, inputs):
        """ 执行远程shell命令，支持多次输入unhashable type: 'list'
        """
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        print(inputs)
        if inputs:
            for input in inputs:
                print(input)
                stdin.write(input + '\n')
        errs = stderr.readlines()
        if errs:
            raise SSHException({errs})
        outs = stdout.readlines()
        return outs

if __name__ == '__main__':
    host = Host()
    print(host)
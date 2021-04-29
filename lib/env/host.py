from dataclasses import dataclass

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
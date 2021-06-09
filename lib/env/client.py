from platon_keys.utils.address import MIANNETHRP, TESTNETHRP

from common.connectServer import connect_linux, run_ssh
from lib.env.mock import mock_connect_linux
from platone import Web3, HTTPProvider, platone, ledger, ledger_node, admin, txpool, user, param, node, personal

from setting import *



failed_msg = "Client-{} do {} failed:{}"
success_msg = "Client-{} do {} success"


class Client():

    def __init__(self, node_conf):


        # self.node = node
        # self.platone = Platone(web3)

        # node server information
        self.host = node_conf["host"]
        self.username = node_conf["username"]
        self.password = node_conf["password"]
        self.ssh_port = node_conf.get("ssh_port", 22)
        self.p2p_port = node_conf["p2p_port"]
        self.rpc_port = node_conf["rpc_port"]
        self.url = node_conf["url"]
        self.node_id = node_conf["node_id"]
        self.node_pubkey = node_conf["node_pubkey"]
        self.chain_id = CHAIN_ID


        self.can_deploy = True
        if self.can_deploy:
            self.ssh, self.sftp, self.t = connect_linux(self.host, self.username, self.password, self.ssh_port)
        else:
            self.ssh, self.sftp, self.t = mock_connect_linux()

        self.web3 = Web3(HTTPProvider(self.url), chain_id=self.chain_id, multi_ledger=True, encryption_mode='SM')

        self.platone = platone.Platone(self.web3)

        self.ledger = ledger.Ledger(self.web3)
        self.ledger.is_wait_receipt = True

        self.ledger_node = ledger_node.LedgerNode(self.web3)
        self.ledger_node.is_wait_receipt = True

        self.admin = admin.Admin(self.web3)

        self.txpool = txpool.TxPool(self.web3)

        self.user = user.User(self.web3)
        self.user.is_wait_receipt = True

        self.param = param.Param(self.web3)
        self.param.is_wait_receipt = True

        self.node = node.Node(self.web3)
        self.node.is_wait_receipt = True

        self.personal = personal.Personal(self.web3)
        self.node_mark = str(self.host) + ":" + str(self.p2p_port)

        if os.path.isabs(linux_put_keystore):
            self.put_keystore_path = "{}/{}".format(linux_put_keystore, wallet_file)
        else:
            self.put_keystore_path = "{}/{}".format(self.pwd, linux_put_keystore)

        self.remote_wallet_file = self.put_keystore_path + "/" + wallet_file




    def try_do(self, func):
        try:
            func()
        except Exception as e:
            raise Exception(failed_msg.format(self.node_mark, func.__name__, e))

    def pwd(self):
        pwd_list = self.run_ssh("pwd")
        pwd = pwd_list[0].strip("\r\n")
        return pwd


    def run_ssh(self, cmd, need_password=False):
        if need_password:
            return run_ssh(self.ssh, cmd, self.password)
        return run_ssh(self.ssh, cmd)



    def put_wallet_file(self):
        """
        Upload wallet file
        :return:
        """
        def __put_wallet_file():
            self.run_ssh("rm -rf {}".format(self.remote_wallet_file))
            self.sftp.put(visitor_wallet_file, self.put_keystore_path)
            self.run_ssh('chmod +x {}'.format(self.remote_wallet_file))
        self.try_do(__put_wallet_file)
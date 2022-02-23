import math
import time, json
import pytest
from hexbytes import HexBytes
from platone import  Account, ledger_node, personal
from platone.platone import Platone

from lib.utils import *
from lib.env.env import *





file_data = LoadFile(ADDRESS_FILE).get_data()
main_address, main_private_key = file_data["main_address"], file_data["main_private_key"]
user_address, user_private_key = file_data["user_address"], file_data["user_private_key"]
chain_admin_address, chain_admin_private_key = file_data["chain_admin_address"], file_data["chain_admin_private_key"]
node_admin_address, node_admin_private_key = file_data["node_admin_address"], file_data["node_admin_private_key"]
contract_admin_address, contract_admin_private_key = file_data["contract_admin_address"], file_data["contract_admin_private_key"]
contract_deployer_address, contract_deployer_private_key = file_data["contract_deployer_address"], file_data["contract_deployer_private_key"]
visitor_address, visitor_private_key = file_data["visitor_address"], file_data["visitor_private_key"]


@pytest.fixture(scope="class", autouse=False)
def global_test_env():
    logger.info("start global_test_env>>>>>>>>>>>>>>")
    test_env = env_factory(NODES_FILE)
    test_env.deploy()
    test_env.parse_client()
    time.sleep(3)
    client = test_env.get_a_consensus_client()
    sys_updatenodetype(client)
    add_users(client)
    result = client.node.update('ROOT-NODE-1', '192.168.16.121', 7789, 17789, '', main_private_key)
    assert_code(result, 0)

    yield test_env



# @pytest.fixture(scope="session", autouse=False)
# def global_test_env():
#     logger.info("start global_test_env>>>>>>>>>>>>>>")
#     test_env = env_factory(NODES_FILE)
#
#     test_env.get_node_file()
#     test_env.parse_client()
#
#     yield test_env




@pytest.fixture()
def clients(global_test_env):

    return global_test_env.get_all_clients()


@pytest.fixture()
def client(global_test_env):
    print('start client--------------------------------fixture')
    client = global_test_env.get_a_consensus_client()
    logger.info(f'client.url = {client.url}')
    return client


@pytest.fixture()
def client_normal(global_test_env):

    return global_test_env.get_a_normal_client()


@pytest.fixture()
def consensus_clients(global_test_env):

    return global_test_env.consensus_client_list()

@pytest.fixture()
def normal_clients(global_test_env):

    return global_test_env.normal_client_list()


@pytest.fixture()
def rand_client(clients):

    return random.choice(clients)





def consensus_client_list(env) -> List[Client]:
    return env.consensus_client_list


@property
def normal_client_list(self) -> List[Client]:
    return self.__normal_client_list



def get_all_clients(self) -> List[Client]:
    """
    Get all client objects
    :return: Client object
    """
    return self.__consensus_client_list + self.__normal_client_list


def get_consensus_client_by_index(self, index) -> Client:
    """
    Get a consensus client based on the index
    :param index:
    :return: Client object
    """
    return self.__consensus_client_list[index]


def get_normal_client_by_index(self, index) -> Client:
    """
    Get a normal client based on the index
    :param index:
    :return: Client object
    """
    return self.__normal_client_list[index]

def get_a_normal_client(self) -> Client:
    """
    Get the first normal client
    :return: Client object
    """
    return self.__normal_client_list[0]

def get_a_consensus_client(self) -> Client:
    """
    Get the first normal client
    :return: Client object
    """
    return self.__consensus_client_list[0]


def get_rand_client(self) -> Client:
    """
    Randomly obtain a consensus client
    :return: Client object
    """
    return random.choice(self.consensus_client_list)






nonexistent_node_id = 'd1b2ca182eca247050e655964850c03b8d6a2bf70c12723ed68b6cab8d45b40abb45b62983d24ea0d213e334763a530d474b1a9089c133774cd1c0d55603d90b'
nonexistent_node_bls_pubkey = '41763655307d6aad1ce1fe7f4789f90a14185b208010da342d60fc902499a361baca0a8d4a0bfa104b7e521be5f62b0f5c6b45d58041017d316b1f535b073535e2da29ea1fb48dda97442970b23a15fdfa8ec45b0f0b810d17a4ed92e69aec19'



def sys_updatenodetype(client):
    node_list = client.node.listAll()
    data = json.loads(node_list[0])['data']
    node_name_list = [data[i]['name'] for i in range(len(data))]
    need_update_nodelist = [name for name in node_name_list if name[-4:] == '7789']
    for name in need_update_nodelist:
        result = client.node.updateType(name, 1, main_private_key)
        assert_code(result, 0)


def add_users(client):
    address = chain_admin_address
    name = '链管理员'
    mobile = '16675161604'
    email = '64216398@qq.com'
    desc = 'node'
    roles = 4611686018427387904
    private_key = main_private_key
    result = client.user.add(address, name, mobile, email, desc, roles, private_key)
    assert_code(result, 0)

    address = node_admin_address
    name = '节点管理员'
    mobile = '16675161604'
    email = '64216398@qq.com'
    desc = 'node'
    roles = 2305843009213693952
    private_key = main_private_key
    result = client.user.add(address, name, mobile, email, desc, roles, private_key)
    assert_code(result, 0)

    address = contract_admin_address
    name = '合约管理员'
    mobile = '16675161604'
    email = '64216398@qq.com'
    desc = 'node'
    roles = 1152921504606846976
    private_key = main_private_key
    result = client.user.add(address, name, mobile, email, desc, roles, private_key)
    assert_code(result, 0)

    address = contract_deployer_address
    name = '合约部署者'
    mobile = '16675161604'
    email = '64216398@qq.com'
    desc = 'node'
    roles = 576460752303423488
    private_key = main_private_key
    result = client.user.add(address, name, mobile, email, desc, roles, private_key)
    assert_code(result, 0)




def transfer(from_privatekey, to_address, amount, ledger, client):
    from_address = Account.privateKeyToAccount(from_privatekey, hrp, mode='SM').address
    nonce = client.platone.getTransactionCount(from_address, ledger=ledger)
    transaction_dict = {
        "to": to_address,
        "gasPrice": client.platone.gasPrice(ledger),
        "gas": 21000,
        "nonce": nonce,
        "data": '',
        "chainId": 200,
        "value": amount,
    }
    logger.info(f'transaction_dict: {transaction_dict}')
    signedTransactionDict = client.platone.account.signTransaction(
        transaction_dict, from_privatekey, net_type=client.web3.net_type, mode='SM'
    )
    data = signedTransactionDict.rawTransaction
    tx_hash = HexBytes(client.platone.sendRawTransaction(data, ledger)).hex()
    result = client.platone.waitForTransactionReceipt(tx_hash, ledger)
    return result


@pytest.fixture()
def transfer_info(client):
    platone = client.platone
    from_address = Account.privateKeyToAccount(main_private_key, hrp, mode='SM').address
    nonce = platone.getTransactionCount(from_address, ledger=sys_ledger)
    transaction_dict = {
        "to": user_address,
        "gasPrice": platone.gasPrice(sys_ledger),
        "gas": 21000,
        "nonce": nonce,
        "data": '',
        "chainId": client.chain_id,
        "value": 1 * 10 ** 18,
    }
    signedTransactionDict = platone.account.signTransaction(
        transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
    )
    data = signedTransactionDict.rawTransaction
    tx_hash = HexBytes(platone.sendRawTransaction(data, sys_ledger)).hex()
    transaction_receipt = platone.waitForTransactionReceipt(tx_hash, sys_ledger)
    block_identifier = transaction_receipt['blockNumber']
    block_hash = transaction_receipt['blockHash']
    transaction_hash = transaction_receipt['transactionHash']
    transaction_index = transaction_receipt['transactionIndex']
    setattr(client, "transaction_receipt", transaction_receipt)
    setattr(client, "block_identifier", block_identifier)
    setattr(client, "block_hash", block_hash)
    setattr(client, "transaction_hash", transaction_hash)
    setattr(client, "transaction_index", transaction_index)
    yield client




def create_oneledger(client):
    nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": client.node_id,
                "nodeType": 1
            }
        ]
    }
    result = client.ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    return ledger_name, sub_ledger_node


def create_twonodes_ledger(client, client_another):
    nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": client.node_id,
                "nodeType": 1
            },
            {
                "PublicKey": client_another.node_id,
                "nodeType": 1
            }
        ]
    }
    result = client.ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    return ledger_name, sub_ledger_node, client

@pytest.fixture()
def create_ledger(client):
    platone = client.platone
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = client.node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            }
        ]
    }
    result = client.ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node, client
    client.ledger.terminateLedger(ledger_name, main_private_key)


@pytest.fixture()
def create_two_ledger(clients):
    client = clients[0]
    another_client = clients[4]
    platone = client.platone
    ledger_name_list = []
    sub_ledger_node_list = []
    for i in range(2):
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        id = client.node_id
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
                {
                    "PublicKey": id,
                    "nodeType": 1
                },
                {
                    "PublicKey": another_client.node_id,
                    "nodeType": 1
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 0)
        logger.info(f'Create ledger {ledger_name} complete')
        sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
        sub_ledger_node.is_wait_receipt = True
        ledger_name_list.append(ledger_name)
        sub_ledger_node_list.append(sub_ledger_node)
    yield ledger_name_list, sub_ledger_node_list, client
    client.ledger.terminateLedger(ledger_name_list[0], main_private_key)
    client.ledger.terminateLedger(ledger_name_list[1], main_private_key)


@pytest.fixture()
def chainadmin_create_ledger(client):
    platone = client.platone
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = client.node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            }
        ]
    }
    result = client.ledger.createLedger(ledger_json, chain_admin_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node, client
    client.ledger.terminateLedger(ledger_name, main_private_key)



@pytest.fixture()
def create_ledger_two_node(clients):
    client, client_another = clients[0], clients[1]
    platone = client.platone
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = client.node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            },
            {
                "PublicKey": client_another.node_id,
                "nodeType": 1
            }
        ]
    }
    result = client.ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node, client
    client.ledger.terminateLedger(ledger_name, main_private_key)


@pytest.fixture()
def create_ledger_three_node(clients):
    client, client_another, client_another2 = clients[0], clients[4], clients[5]
    platone = client.platone
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = client.node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            },
            {
                "PublicKey": client_another.node_id,
                "nodeType": 1
            },
            {
                "PublicKey": client_another2.node_id,
                "nodeType": 1
            }
        ]
    }
    result = client.ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node, client
    client.ledger.terminateLedger(ledger_name, main_private_key)



@pytest.fixture()
def create_ledger_four_node(clients):
    client = clients[0]
    client_another, client_another2, client_another3 = clients[1], clients[4], clients[5]
    platone = client.platone
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = client.node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            },
            {
                "PublicKey": client_another.node_id,
                "nodeType": 1
            },
            {
                "PublicKey": client_another2.node_id,
                "nodeType": 1
            },
            {
                "PublicKey": client_another3.node_id,
                "nodeType": 1
            }
        ]
    }
    result = client.ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node, client
    client.ledger.terminateLedger(ledger_name, main_private_key)


@pytest.fixture()
def create_ledger_jion_consensus_node(create_ledger, clients):
    ledger_name, sub_ledger_node, client = create_ledger
    client_another = clients[1]
    join_result = client.ledger.joinLedger(ledger_name, client_another.node_id, client_another.node_pubkey, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(client_another.node_id, client_another.node_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {client_another.url} to complete')
    yield ledger_name, sub_ledger_node, client


@pytest.fixture()
def create_ledger_jion_observe_node(create_ledger, clients):
    ledger_name, sub_ledger_node, client = create_ledger
    observe_client_another = clients[4]
    join_result = client.ledger.joinLedger(ledger_name, observe_client_another.node_id, observe_client_another.node_pubkey, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(observe_client_another.node_id, observe_client_another.node_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {observe_client_another.url} to complete')
    yield ledger_name, sub_ledger_node, client


@pytest.fixture()
def create_ledger_jion_two_node(create_ledger, clients):
    ledger_name, sub_ledger_node, client = create_ledger
    client_anther, client_anther2 = clients[4], clients[1]
    join_result = client.ledger.joinLedger(ledger_name, client_anther.node_id, client_anther.node_pubkey, main_private_key)
    assert_code(join_result, 0)
    join_result = client.ledger.joinLedger(ledger_name, client_anther2.node_id, client_anther2.node_pubkey, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(client_anther.node_id, client_anther.node_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {client_anther.url} to complete')
    add_result = sub_ledger_node.add(client_anther2.node_id, client_anther2.node_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {client_anther2.url} to complete')
    yield ledger_name, sub_ledger_node, client

    
@pytest.fixture()
def create_ledger_jion_three_node(create_ledger, clients):
    ledger_name, sub_ledger_node, client = create_ledger
    client_anther, client_anther2, client_anther3 = clients[4], clients[5], clients[1]
    join_result = client.ledger.joinLedger(ledger_name, client_anther.node_id, client_anther.node_pubkey, main_private_key)
    assert_code(join_result, 0)
    join_result = client.ledger.joinLedger(ledger_name, client_anther2.node_id, client_anther2.node_pubkey, main_private_key)
    assert_code(join_result, 0)
    join_result = client.ledger.joinLedger(ledger_name, client_anther3.node_id, client_anther3.node_pubkey, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(client_anther.node_id, client_anther.node_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node client{client_anther.url} to complete')
    add_result = sub_ledger_node.add(client_anther2.node_id, client_anther2.node_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {client_anther2.url} to complete')
    add_result = sub_ledger_node.add(client_anther3.node_id, client_anther3.node_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {client_anther3.url} to complete')
    yield ledger_name, sub_ledger_node, client


def wait_settlement(platone: Platone, ledger = sys_ledger, settlement=0):
    """
    Waiting for a billing cycle to settle
    :param node:
    :param number: number of billing cycles
    :return:
    """
    block_number = 250 * settlement
    tmp_current_block = platone.blockNumber(ledger)
    current_end_block = math.ceil(tmp_current_block / 250) * 250 + block_number

    current_block = platone.blockNumber(ledger)
    if 0 < current_end_block - current_block <= 10:
        timeout = 10 + int(time.time()) + 50
    elif current_end_block - current_block > 10:
        timeout = int((current_end_block - current_block) * 1 * 1.5) + int(time.time()) + 50
    else:
        logger.info('current block {} is greater than block {}'.format(platone.blockNumber(ledger), current_end_block))
        return
    print_t = 0
    while int(time.time()) < timeout:
        print_t += 1
        if print_t == 10:
            # Print once every 10 seconds to avoid printing too often
            logger.info(
                '{}: The current block height is {}, waiting until {}'.format('192.168.16.122:7789', platone.blockNumber(ledger), current_end_block))
            print_t = 0
        if platone.blockNumber(ledger) > current_end_block:
            return
        time.sleep(1)
    raise Exception("Unable to pop out the block normally, the "
                    "current block height is: {}, the target block height is: {}".format(platone.blockNumber(ledger), current_end_block))

@pytest.fixture()
def produce_empty_block(create_ledger):
    ledger_name, _, client = create_ledger
    update_result = client.param.updateIsProduceEmptyBlock(True, main_private_key)
    assert_code(update_result, 0)
    logger.info('Set empty block successfully')
    time.sleep(3)
    blocknumber = client.platone.blockNumber(sys_ledger)
    blocknumber_subledger = client.platone.blockNumber(ledger_name)
    time.sleep(3)
    blocknumber_after = client.platone.blockNumber(sys_ledger)
    blocknumber_subledger_after = client.platone.blockNumber(ledger_name)
    assert 0 < blocknumber_after - blocknumber < 6 and 1 < blocknumber_subledger_after - blocknumber_subledger < 6
    yield ledger_name, client


@pytest.fixture()
def not_produce_empty_block(create_ledger):
    ledger_name, _, client = create_ledger
    update_result = client.param.updateIsProduceEmptyBlock(False, main_private_key)
    assert_code(update_result, 0)
    blocknumber = client.platone.blockNumber(sys_ledger)
    blocknumber_subledger = client.platone.blockNumber(ledger_name)
    time.sleep(5)
    blocknumber_after = client.platone.blockNumber(sys_ledger)
    blocknumber_subledger_after = client.platone.blockNumber(ledger_name)
    assert blocknumber_after == blocknumber
    assert blocknumber_subledger_after == blocknumber_subledger
    logger.info('No empty block is set successfully ')
    yield ledger_name, client
    update_result = client.param.updateIsProduceEmptyBlock(True, main_private_key)
    assert_code(update_result, 0)
    logger.info('Cannot set empty block successfully ')


def assert_blocknumber_growth(sys_ledger, ledger_name, client):
    blocknumber = client.platone.blockNumber(sys_ledger)
    sub_blocknumber = client.platone.blockNumber(ledger_name)
    time.sleep(3)
    blocknumber_wait = client.platone.blockNumber(sys_ledger)
    sub_blocknumber_wait = client.platone.blockNumber(ledger_name)
    sub_blockhigh_growth = sub_blocknumber_wait - sub_blocknumber
    sys_blockhigh_growth = blocknumber_wait - blocknumber
    assert 0 < blocknumber_wait - blocknumber < 6 and 0 < sub_blocknumber_wait - sub_blocknumber < 6
    assert abs(sub_blockhigh_growth - sys_blockhigh_growth) <= 2



def assert_not_produce_empty_block(sys_ledger, ledger_name, client):
    sub_blocknumber = client.platone.blockNumber(ledger_name)
    sys_blocknumber = client.platone.blockNumber(sys_ledger)
    time.sleep(3)
    sub_blocknumber_after = client.platone.blockNumber(ledger_name)
    sys_blocknumber_after = client.platone.blockNumber(sys_ledger)
    sub_blockhigh_growth = sub_blocknumber_after - sub_blocknumber
    sys_blockhigh_growth = sys_blocknumber_after - sys_blocknumber
    assert abs(sub_blockhigh_growth - sys_blockhigh_growth) == 0

def assert_sys_blocknumber_growth_sub_notgrowth(sys_ledger, ledger_name, client):
    sub_blocknumber = client.platone.blockNumber(ledger_name)
    sys_blocknumber = client.platone.blockNumber(sys_ledger)
    time.sleep(3)
    sub_blocknumber_after = client.platone.blockNumber(ledger_name)
    sys_blocknumber_after = client.platone.blockNumber(sys_ledger)
    sub_blockhigh_growth = sub_blocknumber_after - sub_blocknumber
    sys_blockhigh_growth = sys_blocknumber_after - sys_blocknumber
    assert 0 < sys_blockhigh_growth < 6 and sub_blockhigh_growth == 0


def assert_sys_blocknumber_notgrowth_sub_growth(sys_ledger, ledger_name, client):
    sub_blocknumber = client.platone.blockNumber(ledger_name)
    sys_blocknumber = client.platone.blockNumber(sys_ledger)
    time.sleep(3)
    sub_blocknumber_after = client.platone.blockNumber(ledger_name)
    sys_blocknumber_after = client.platone.blockNumber(sys_ledger)
    sub_blockhigh_growth = sub_blocknumber_after - sub_blocknumber
    sys_blockhigh_growth = sys_blocknumber_after - sys_blocknumber
    assert 0 < sub_blockhigh_growth < 6 and sys_blockhigh_growth == 0


def assert_sys_sub_blocknumber_notgrowth(sys_ledger, ledger_name, client):
    sub_blocknumber = client.platone.blockNumber(ledger_name)
    sys_blocknumber = client.platone.blockNumber(sys_ledger)
    time.sleep(3)
    sub_blocknumber_after = client.platone.blockNumber(ledger_name)
    sys_blocknumber_after = client.platone.blockNumber(sys_ledger)
    sub_blockhigh_growth = sub_blocknumber_after - sub_blocknumber
    sys_blockhigh_growth = sys_blocknumber_after - sys_blocknumber
    assert sub_blockhigh_growth == 0 and sys_blockhigh_growth == 0





if __name__ == '__main__':
    pass
import math
import time, json

import pytest
from hexbytes import HexBytes
from platone import Web3, HTTPProvider, platone, txpool, Account, miner, net, personal, ledger, ledger_node, admin, user
from lib.utils import *
from loguru import logger
from platone.platone import Platone

#todo: 这些等瓜攀弄好环境再整
# rpc = 'http://10.10.8.209:6999'
rpc = 'http://192.168.16.122:7789'
rpc_another = 'http://192.168.16.124:7789'
rpc_another121 = 'http://192.168.16.121:7789'
rpc_another123 = 'http://192.168.16.123:7789'
chain_id = 200
hrp = 'lax'
sys_ledger = 'sys'
# main_address, main_private_key = 'lax1jt7m9cs9ryqtqpt939yvhxlqfqc3dscdtvgx8k', 'f90fd6808860fe869631d978b0582bb59db6189f7908b578a886d582cb6fccfa'
# user_address, user_private_key = 'lax1apg69eyemch5hxsfw4e2kj94e92la7vt2ucuwr', 'a98e6baea6233965a0740e20e626c5500ecf16121547e8255ee5a28a4f08fc57'
main_address, main_private_key = 'lax1dqd2gg9s634e2m72e70s2u5hh0vd474epxqmtm', '72235584de46e7b2a06fca02f1eb710f3cc7050c940160558c5331ca77340bcf'
user_address, user_private_key = 'lax1yyc4fcrqmfw9g3urw7t7jj4qwp4cfmwpl5g705', '802158ca03ed58d0115d4d84e325c312521629be3afbbe08a12de641b5f59b92'
chain_admin_address, chain_admin_private_key = 'lax1u2rlvu2x545r84yjw6hcgewe9axmmgp9tc4yne', 'adb0fa48bbba6f4e64e1b9517d3a67378399d48d5c6a2509972bb7758ad1f8fa'
node_admin_address, node_admin_private_key = 'lax1lwhhmxm9pxqj6k9ev35psvzf4lxyx625pgeh0z', '3d3a16b247bc8064833e2e6a131cdb61e9587dd9c8c6564196c0e459a6ffa526'
contract_admin_address, contract_admin_private_key = 'lax1m7qam7mxk3zwtj4vkwr2zfstuzmy4u3xaxhlxn', 'f9329cb010460afb375f19093ac886e4a10a7d9dbe02e903d91e519b94199207'
contract_deployer_address, contract_deployer_private_key = 'lax139kdt6lc5f2npcmvxvwg89q9khf8zdg3cyxq6s', '3152b678c37ab821644ac82812d0f00b281cb58e5d658b695ef8c5610a4da726'
visitor_address, visitor_private_key = 'lax1hg4pa8vpqzd8c2ncz39kvvpq7hgn9pc7pmusjd', '242db3a9a14d5345e23caee4ac0e705f1489efa487e4cfddcf44ef9d64895f11'

# w3 = Web3(HTTPProvider(rpc), chain_id=chain_id)
w3 = Web3(HTTPProvider(rpc), chain_id=chain_id, multi_ledger=True, encryption_mode='SM')
platone = platone.Platone(w3)

txpool = txpool.TxPool(w3)
net = net.Net(w3)
personal = personal.Personal(w3)
ledger =ledger.Ledger(w3)
ledger.is_wait_receipt = True
node = ledger_node.LedgerNode(w3, 'sys')
node.is_wait_receipt = True
admin_ledger = admin.Admin(w3)

node_info = admin_ledger.nodeInfo
root_node_id = node_info['id']
root_node_bls_pubkey = node_info['blsPubKey']

w3_anther = Web3(HTTPProvider(rpc_another), chain_id=chain_id, multi_ledger=True, encryption_mode='SM')
admin_anther = admin.Admin(w3_anther)
another_node_info = admin_anther.nodeInfo
another_node_id = another_node_info['id']
another_node_bls_pubkey = another_node_info['blsPubKey']

w3_anther121 = Web3(HTTPProvider(rpc_another121), chain_id=chain_id, multi_ledger=True, encryption_mode='SM')
admin_anther121 = admin.Admin(w3_anther121)
another_node_info121 = admin_anther121.nodeInfo
another_node_id121 = another_node_info121['id']
another_node_bls_pubkey121 = another_node_info121['blsPubKey']

w3_anther123 = Web3(HTTPProvider(rpc_another123), chain_id=chain_id, multi_ledger=True, encryption_mode='SM')
admin_anther123 = admin.Admin(w3_anther123)
another_node_info123 = admin_anther123.nodeInfo
another_node_id123 = another_node_info123['id']
another_node_bls_pubkey123 = another_node_info123['blsPubKey']

nonexistent_node_id = 'd1b2ca182eca247050e655964850c03b8d6a2bf70c12723ed68b6cab8d45b40abb45b62983d24ea0d213e334763a530d474b1a9089c133774cd1c0d55603d90b'
nonexistent_node_bls_pubkey = '41763655307d6aad1ce1fe7f4789f90a14185b208010da342d60fc902499a361baca0a8d4a0bfa104b7e521be5f62b0f5c6b45d58041017d316b1f535b073535e2da29ea1fb48dda97442970b23a15fdfa8ec45b0f0b810d17a4ed92e69aec19'


user = user.User(w3)
user.is_wait_receipt = True




def transfer(from_privatekey, to_address, amount, ledger):
    from_address = Account.privateKeyToAccount(from_privatekey, hrp, mode='SM').address
    nonce = platone.getTransactionCount(from_address, ledger=ledger)
    transaction_dict = {
        "to": to_address,
        "gasPrice": platone.gasPrice(ledger),
        "gas": 21000,
        "nonce": nonce,
        "data": '',
        "chainId": chain_id,
        "value": amount,
    }
    logger.info(f'transaction_dict: {transaction_dict}')
    signedTransactionDict = platone.account.signTransaction(
        transaction_dict, from_privatekey, net_type=w3.net_type, mode='SM'
    )
    data = signedTransactionDict.rawTransaction
    tx_hash = HexBytes(platone.sendRawTransaction(data, ledger)).hex()
    result = platone.waitForTransactionReceipt(tx_hash, ledger)
    return result


@pytest.fixture()
def transfer_info():
    from_address = Account.privateKeyToAccount(main_private_key, hrp, mode='SM').address
    nonce = platone.getTransactionCount(from_address, ledger=sys_ledger)
    transaction_dict = {
        "to": user_address,
        "gasPrice": platone.gasPrice(sys_ledger),
        "gas": 21000,
        "nonce": nonce,
        "data": '',
        "chainId": chain_id,
        "value": 1 * 10 ** 18,
    }
    signedTransactionDict = platone.account.signTransaction(
        transaction_dict, main_private_key, net_type=w3.net_type, mode='SM'
    )
    data = signedTransactionDict.rawTransaction
    tx_hash = HexBytes(platone.sendRawTransaction(data, sys_ledger)).hex()
    transaction_receipt = platone.waitForTransactionReceipt(tx_hash, sys_ledger)
    block_identifier = transaction_receipt['blockNumber']
    block_hash = transaction_receipt['blockHash']
    transaction_hash = transaction_receipt['transactionHash']
    transaction_index = transaction_receipt['transactionIndex']
    setattr(platone, "transaction_receipt", transaction_receipt)
    setattr(platone, "block_identifier", block_identifier)
    setattr(platone, "block_hash", block_hash)
    setattr(platone, "transaction_hash", transaction_hash)
    setattr(platone, "transaction_index", transaction_index)
    yield platone




def create_oneledger():
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = root_node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            }
        ]
    }
    result = ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    return ledger_name, sub_ledger_node

@pytest.fixture()
def create_ledger():
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = root_node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            }
        ]
    }
    result = ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    # sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
    # sub_ledger_node.is_wait_receipt = True
    # yield ledger_name, sub_ledger_node
    # ledger.terminateLedger(ledger_name, main_private_key)


@pytest.fixture()
def create_two_ledger():
    ledger_name_list = []
    sub_ledger_node_list = []
    for i in range(2):
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        id = root_node_id
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
                {
                    "PublicKey": id,
                    "nodeType": 1
                }
            ]
        }
        result = ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 0)
        logger.info(f'Create ledger {ledger_name} complete')
        sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
        sub_ledger_node.is_wait_receipt = True
        ledger_name_list.append(ledger_name)
        sub_ledger_node_list.append(sub_ledger_node)
    yield ledger_name_list, sub_ledger_node_list
    # ledger.terminateLedger(ledger_name_list[0], main_private_key)
    # ledger.terminateLedger(ledger_name_list[1], main_private_key)


@pytest.fixture()
def chainadmin_create_ledger():
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = root_node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            }
        ]
    }
    result = ledger.createLedger(ledger_json, chain_admin_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node
    ledger.terminateLedger(ledger_name, main_private_key)



@pytest.fixture()
def create_ledger_two_node():
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = root_node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            },
            {
                "PublicKey": another_node_id,
                "nodeType": 1
            }
        ]
    }
    result = ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node
    ledger.terminateLedger(ledger_name, main_private_key)


@pytest.fixture()
def create_ledger_three_node():
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = root_node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            },
            {
                "PublicKey": another_node_id,
                "nodeType": 1
            },
            {
                "PublicKey": another_node_id121,
                "nodeType": 1
            }
        ]
    }
    result = ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node
    ledger.terminateLedger(ledger_name, main_private_key)

@pytest.fixture()
def create_ledger_four_node():
    nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
    ledger_name = "test" + str(nonce)
    id = root_node_id
    ledger_json = {
        "LedgerName": ledger_name,
        "NodeLedgerInfos": [
            {
                "PublicKey": id,
                "nodeType": 1
            },
            {
                "PublicKey": another_node_id,
                "nodeType": 1
            },
            {
                "PublicKey": another_node_id121,
                "nodeType": 1
            },
            {
                "PublicKey": another_node_id123,
                "nodeType": 1
            }
        ]
    }
    result = ledger.createLedger(ledger_json, main_private_key)
    assert_code(result, 0)
    logger.info(f'Create ledger {ledger_name} complete')
    sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
    sub_ledger_node.is_wait_receipt = True
    yield ledger_name, sub_ledger_node
    ledger.terminateLedger(ledger_name, main_private_key)


@pytest.fixture()
def create_ledger_jion_consensus_node(create_ledger):
    ledger_name, sub_ledger_node = create_ledger
    join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {another_node_id} to complete')
    yield ledger_name, sub_ledger_node


@pytest.fixture()
def create_ledger_jion_observe_node(create_ledger):
    ledger_name, sub_ledger_node = create_ledger
    join_result = ledger.joinLedger(ledger_name, another_node_id121, another_node_bls_pubkey121, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey121, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {another_node_id121} to complete')
    yield ledger_name, sub_ledger_node


@pytest.fixture()
def create_ledger_jion_two_node(create_ledger):
    ledger_name, sub_ledger_node = create_ledger
    join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {another_node_id} to complete')
    add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey121, main_private_key)
    assert_code(add_result, 0)
    yield ledger_name, sub_ledger_node

    
@pytest.fixture()
def create_ledger_jion_three_node(create_ledger):
    ledger_name, sub_ledger_node = create_ledger
    join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
    assert_code(join_result, 0)
    time.sleep(3)
    add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
    assert_code(add_result, 0)
    logger.info(f'Ledger {ledger_name} joins node {another_node_id} to complete')
    add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey121, main_private_key)
    assert_code(add_result, 0)
    add_result = sub_ledger_node.add(another_node_id123, another_node_bls_pubkey123, main_private_key)
    assert_code(add_result, 0)
    yield ledger_name, sub_ledger_node


def wait_settlement(platone: Platone, settlement=0):
    """
    Waiting for a billing cycle to settle
    :param node:
    :param number: number of billing cycles
    :return:
    """
    block_number = 40 * settlement
    tmp_current_block = platone.blockNumber(sys_ledger)
    current_end_block = math.ceil(tmp_current_block / 250) * 250 + block_number

    current_block = platone.blockNumber(sys_ledger)
    if 0 < current_end_block - current_block <= 10:
        timeout = 10 + int(time.time()) + 50
    elif current_end_block - current_block > 10:
        timeout = int((current_end_block - current_block) * 1 * 1.5) + int(time.time()) + 50
    else:
        logger.info('current block {} is greater than block {}'.format(platone.blockNumber(sys_ledger), current_end_block))
        return
    print_t = 0
    while int(time.time()) < timeout:
        print_t += 1
        if print_t == 10:
            # Print once every 10 seconds to avoid printing too often
            logger.info(
                '{}: The current block height is {}, waiting until {}'.format('192.168.16.122:7789', platone.blockNumber(sys_ledger), current_end_block))
            print_t = 0
        if platone.blockNumber(sys_ledger) > current_end_block:
            return
        time.sleep(1)
    raise Exception("Unable to pop out the block normally, the "
                    "current block height is: {}, the target block height is: {}".format(platone.blockNumber(sys_ledger), current_end_block))


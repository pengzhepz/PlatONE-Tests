
import pytest, time
from platone import Web3, HTTPProvider, platone, txpool, Account, miner, net, personal, ledger, ledger_node, admin
from lib.utils import *
from cases.ledger.conftest import *
from loguru import logger




class TestCreatLedger():

    def test_create_ledger(self):
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
        len_list = len(json.loads(ledger.getAllLedgers()[0])['data'])
        for i in range(len_list):
            if ledger_name == json.loads(ledger.getAllLedgers()[0])['data'][i]['LedgerName']:
                assert json.loads(ledger.getAllLedgers()[0])['data'][i]['ConsensusNodes'][0]['blsPubKey'] == root_node_bls_pubkey
                break
        else:
            assert 1 == 2, 'Failed to create ledger'


    def test_create_ledger_observer_node(self):
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        id = another_node_id
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
        assert_code(result, 305010)


    def test_create_ledger_same_name(self):
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
        result = ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 305004)


    def test_create_ledger_same_node(self):
        for i in range(3):
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


    def test_create_ledger_nonexistent_node(self):
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        id = nonexistent_node_id
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
        assert_code(result, 305009)


    def test_create_ledger_several_node(self):
        """
        todo:确认下nodeType各个数字代表什么
        """
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

        add_nodes_list = [root_node_bls_pubkey, another_node_bls_pubkey, another_node_bls_pubkey121, another_node_bls_pubkey123]
        len_list = len(json.loads(ledger.getAllLedgers()[0])['data'])
        for i in range(len_list):
            if ledger_name == json.loads(ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                len_consensus_nodes = len(json.loads(ledger.getAllLedgers()[0])['data'][i]['consensusNodes'])
                for j in range(len_consensus_nodes):
                    node_blspubkey = json.loads(ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][j]['blsPubKey']
                    if node_blspubkey in add_nodes_list:
                        add_nodes_list.remove(node_blspubkey)
                assert len(add_nodes_list) == 0
                break
        else:
            assert 1 == 2, 'Failed to create ledger'



    def test_create_ledger_several_observe_node(self):
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
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
        assert_code(result, 305010)


    def test_create_ledger_several_same_node(self):
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
                    },
                    {
                        "PublicKey": another_node_id,
                        "nodeType": 1
                    },
                ]
            }
            result = ledger.createLedger(ledger_json, main_private_key)
            assert_code(result, 0)



    def test_create_ledger_several_nonexistent_node(self):
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
                    "PublicKey": nonexistent_node_id,
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
        assert_code(result, 305009)



class TestJoinLedger():

    def test_join_ledger(self, create_ledger_jion_consensus_node):
        ledger_name, sub_ledger_node = create_ledger_jion_consensus_node
        jion_nodeid = json.loads(sub_ledger_node.list()[0])['data'][0]['observer']['nodeID']
        assert jion_nodeid == another_node_id


    def test_join_ledger_observer(self, create_ledger):
        """

        """
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey123, main_private_key)
        assert_code(add_result, 0)
        jion_nodeid = json.loads(sub_ledger_node.list()[0])['data'][0]['observer']['nodeID']
        assert jion_nodeid == another_node_id121


    def test_join_ledger_nonexistent_node(self, create_ledger):
        #todo: 可以添加进去，这是不是Bug啊，添加进去之后权限呢？
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, nonexistent_node_id, nonexistent_node_bls_pubkey, main_private_key)
        assert_code(join_result, 301019)
        time.sleep(3)
        add_result = sub_ledger_node.add(nonexistent_node_id, nonexistent_node_bls_pubkey, main_private_key)
        assert_code(add_result, 0)


    def test_join_nonexistent_ledger(self):
        ledger_name = 'xxxxxxxx'
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 305005)
        print(join_result)
        time.sleep(3)
        sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
        sub_ledger_node.is_wait_receipt = True
        status = True
        try:
            add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
        except:
            status = False
        assert status == False



    def test_join_ledger_repeat(self, create_ledger_jion_consensus_node):
        ledger_name, sub_ledger_node = create_ledger_jion_consensus_node
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 305013)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(add_result, 306012)



class TestQuitLedger():

    def test_quit_ledger(self, create_ledger_jion_observe_node):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(result, 0)
        time.sleep(2)
        result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(result, 0)

    def test_quit_nonexistent_ledger(self, create_ledger_jion_observe_node):
        _, _ = create_ledger_jion_observe_node
        ledger_name = 'xxxxxxx'
        result = ledger.quitLedger(ledger_name, another_node_id123, main_private_key)
        assert_code(result, 305005)
        sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
        sub_ledger_node.is_wait_receipt = True
        status = True
        try:
            result = sub_ledger_node.remove(another_node_id123, main_private_key)
        except:
            status = False
        assert status == False



    def test_quit_ledger_nonexistent_node(self, create_ledger_jion_observe_node):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        result = ledger.quitLedger(ledger_name, another_node_id123, main_private_key)
        assert_code(result, 305014)
        result = sub_ledger_node.remove(another_node_id123, main_private_key)
        assert_code(result, 306008)


    def test_quit_ledger_repeat(self, create_ledger_jion_observe_node):
        #todo: assert_code(result, 305016) 返回码应该是305014，而不是305016'Cannot quit the last node'
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(result, 0)

        result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(result, 305016)
        result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(result, 306008)


    def test_quit_ledger_consensus(self, create_ledger_two_node):
        #todo: 应该是报错不是超时吧？
        ledger_name, sub_ledger_node = create_ledger_two_node
        result = ledger.quitLedger(ledger_name, another_node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(another_node_id, main_private_key)
        # assert_code(result, 306008)
        print(result)


    def test_quit_ledger_consensus_to_observer(self, create_ledger_four_node):
        #todo: 预期成功
        ledger_name, sub_ledger_node = create_ledger_four_node
        time.sleep(5)
        result = sub_ledger_node.updateNodeType(another_node_id121, 2, main_private_key)
        assert_code(result, 0)
        time.sleep(10)
        result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(another_node_id121, main_private_key)
        print(result)


    def test_quit_ledger_consensus_to_observer_not_effective(self, create_ledger_two_node):
        ledger_name, sub_ledger_node = create_ledger_two_node
        time.sleep(10)
        node_list = sub_ledger_node.list()
        print(node_list)
        rersult = sub_ledger_node.updateNodeType(another_node_id, 2, main_private_key)
        print(rersult)
        time.sleep(10)
        node_list = sub_ledger_node.list()
        print(node_list)



class TestTerminateLedger():

    def test_terminate_ledger(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        len_list_befor = len(json.loads(ledger.getAllLedgers()[0])['data'])
        ledger_list_befor = [json.loads(ledger.getAllLedgers()[0])['data'][i]['ledgerName'] for i in range(len_list_befor)]
        assert ledger_name in ledger_list_befor

        result = ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        len_list_after = len(json.loads(ledger.getAllLedgers()[0])['data'])
        ledger_list_after = [json.loads(ledger.getAllLedgers()[0])['data'][i]['ledgerName'] for i in range(len_list_after)]
        assert ledger_name not in ledger_list_after
        assert len_list_befor - len_list_after == 1
        status = False
        try:
            result = sub_ledger_node.list()
        except:
            status = True
        assert status


    def test_terminate_ledger_several_node(self, create_ledger_four_node):
        ledger_name, sub_ledger_node = create_ledger_four_node
        ledger_list = [json.loads(ledger.getAllLedgers()[0])['data'][i]['ledgerName'] for i in range(len(json.loads(ledger.getAllLedgers()[0])['data']))]
        assert ledger_name in ledger_list
        result = ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        print(ledger.getAllLedgers())
        ledger_list = [json.loads(ledger.getAllLedgers()[0])['data'][i]['ledgerName'] for i in range(len(json.loads(ledger.getAllLedgers()[0])['data']))]
        assert ledger_list == []
        status = False
        try:
            result = sub_ledger_node.list()
        except:
            status = True
        assert status


    def test_terminate_ledger_nonexistent(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        nonexistent_ledger_name = 'xxxxxxx'
        result = ledger.terminateLedger(nonexistent_ledger_name, main_private_key)
        assert_code(result, 305005)


    def test_terminate_ledger_repeat(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        result = ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        repeat_result = ledger.terminateLedger(ledger_name, main_private_key)
        print(repeat_result)



    def test_terminate_ledger_nonexistent_node(self, create_ledger):
        #todo: 场景没有造
        ledger_name, _ = create_ledger
        sub_ledger_node = ledger_node.LedgerNode(w3, ledger_name)
        sub_ledger_node.is_wait_receipt = True



    def test_terminate_repeatedly(self):
        for i in range(40):
            ledger_name, _ = create_oneledger()
            print(f'i: ledger_name: {i, ledger_name}')
            time.sleep(2)
            result = ledger.terminateLedger(ledger_name, main_private_key)
            print(result)



class TestUpdateNodeType():


    def test_updatenodetype(self, create_ledger_jion_observe_node):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == another_node_id121
        result = sub_ledger_node.updateNodeType(another_node_id121, 1, main_private_key)
        assert_code(result, 0)
        consensus_node_list = [json.loads(sub_ledger_node.list()[0])['data']['consensus'][i]['nodeID'] for i in range(len(json.loads(sub_ledger_node.list()[0])['data']['consensus']))]
        assert another_node_id121 in consensus_node_list


    def test_updatenodetype_con_to_obs(self, create_ledger_four_node):
        ledger_name, sub_ledger_node = create_ledger_four_node
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []
        result = sub_ledger_node.updateNodeType(another_node_id121, 2, main_private_key)
        assert_code(result, 0)
        sub_ledger_list = sub_ledger_node.list()
        update_obs_nodeid = json.loads(sub_ledger_list[0])['data']['observer'][0]['nodeID']
        assert update_obs_nodeid == another_node_id121


    def test_updatenodetype_con_to_obs_border(self, create_ledger_three_node):
        ledger_name, sub_ledger_node = create_ledger_three_node
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []
        result = sub_ledger_node.updateNodeType(another_node_id121, 2, main_private_key)
        assert_code(result, 0)
        sub_ledger_list = sub_ledger_node.list()
        update_obs_nodeid = json.loads(sub_ledger_list[0])['data']['observer'][0]['nodeID']
        assert update_obs_nodeid == another_node_id121


    def test_updateNodeType_con_to_obs_less(self, create_ledger_two_node):
        """
        todo: 预期是修改失败的,但是修改成功了,这个限制好像只在ptool管理台做了限制
        """
        ledger_name, sub_ledger_node = create_ledger_two_node
        time.sleep(10)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []
        node_list = sub_ledger_node.list()
        print(node_list)

        result = sub_ledger_node.updateNodeType(another_node_id, 2, main_private_key)
        # assert_code(result, 0)
        print(result)

        time.sleep(10)
        # update_obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        # assert update_obs_nodeid == obs_nodeid
        node_list = sub_ledger_node.list()
        print(node_list)



    def test_updatenodetype_onlycon_to_obs(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(10)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []
        result = sub_ledger_node.updateNodeType(root_node_id, 2, main_private_key)
        assert_code(result, 306011)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []


class TestGrantRrevokePerm():

    def test_grantperm(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)

    def test_grantperm_repeat(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)
        time.sleep(3)
        repeat_grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        #todo: 应该是要加个判断不能一直这样的吧？
        assert_code(repeat_grantperm_result, 0)
        print(repeat_grantperm_result)


    def test_revokeperm(self, create_ledger):
        #todo: 没有授权地址也可以直接回收权限，是不是要改一下？好像也影响不大
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)
        time.sleep(3)
        grantperm_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)


    def test_nogrant_revokeperm(self, create_ledger):
        #todo: 没有授权地址也可以直接回收权限，是不是要改一下？好像也影响不大
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)


    def test_revokeperm_repeat(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)
        time.sleep(3)
        revoke_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(revoke_result, 0)
        time.sleep(3)
        repeat_revoke_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        # todo: 应该是要加个判断不能一直这样的吧？
        assert_code(repeat_revoke_result, 0)
        print(repeat_revoke_result)



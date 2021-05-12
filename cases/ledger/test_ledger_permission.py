from cases.ledger.conftest import *



# address = 'lax1un3hk529f0y793yrnf3ccch5rfe40rsede2tre'
# name = 'test001'
# mobile = '18665851938'
# email = '64216398@qq.com'
# desc = 'nodeaaa'
# roles = '1'
# private_key = main_private_key
# result = user.add()
# print(result)

class TestCreateLedger():


    def test_chain_admin_create_ledger(self):
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
        len_list = len(json.loads(ledger.getAllLedgers()[0])['data'])
        for i in range(len_list):
            if ledger_name == json.loads(ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                assert json.loads(ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][0][
                           'blsPubKey'] == root_node_bls_pubkey
                break
        else:
            assert 1 == 2, 'Failed to create ledger'

    @pytest.mark.parametrize('sign_user', [node_admin_private_key, contract_admin_private_key, contract_deployer_private_key, visitor_private_key])
    def test_node_admin_create_ledger(self, sign_user):
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
        result = ledger.createLedger(ledger_json, sign_user)
        assert_code(result, 305003)
        ledger_list = [json.loads(ledger.getAllLedgers()[0])['data'][i]['ledgerName'] for i in range(len(json.loads(ledger.getAllLedgers()[0])['data']))]
        assert ledger_name not in ledger_list


class TestJoinLedger():



    def test_chain_admin_join_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 0)
        jion_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert jion_nodeid == another_node_id


    def test_chaincreator_join_chainadmin_create_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(add_result, 306006)



    def test_chaincreator_join_chainadmin_create_authorized_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger

        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(add_result, 0)

        result = sub_ledger_node.grantPerm(chain_admin_address, chain_admin_private_key)
        print(result)
        time.sleep(5)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
        # assert_code(add_result, 0)
        print(add_result)
        jion_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert jion_nodeid == another_node_id


    def test_chaincreator_join_chainadmin_create_grant_revoke_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 0)
        grant_result = sub_ledger_node.grantPerm(chain_admin_address, chain_admin_private_key)
        assert_code(grant_result, 0)
        revoke_result = sub_ledger_node.revokePerm(chain_admin_address, chain_admin_private_key)
        assert_code(revoke_result, 0)
        time.sleep(2)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(add_result, 306006)




    def test_chain_admin_join_chaincreator_nopermission_ledger(self, create_ledger):
        #todo: sdk里面关于encode_abi的arguments[j] = addr  # .split(",")错误 TypeError: 'tuple' object does not support item assignment
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 306006)


    def test_chain_admin_join_chaincreator_authorized_ledger(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 306006)
        grant_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(2)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 0)


    def test_chain_admin_join_chaincreator_grant_revoke_ledger(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        grant_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grant_result, 0)
        revoke_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(revoke_result, 0)
        time.sleep(2)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 306006)


    @pytest.mark.parametrize('sign_user', [node_admin_private_key, contract_admin_private_key, contract_deployer_private_key, visitor_private_key])
    def test_nopermission_join_ledger(self, create_ledger, sign_user):
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, sign_user)
        assert_code(join_result, 305003)




class TestQuitLedger():


    def test_chaincreator_quit_chainadmin_create_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 0)
        time.sleep(5)
        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(quitledger_result, 0)
        remove_result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(remove_result, 306006)


    def test_chaincreator_quit_chainadmin_create_authorized_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 0)
        time.sleep(5)

        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(quitledger_result, 0)
        remove_result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(remove_result, 306006)
        grant_result = sub_ledger_node.grantPerm(main_address, chain_admin_private_key)
        assert_code(grant_result, 0)
        time.sleep(2)
        result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(result, 0)


    def test_chaincreator_quit_chainadmin_create_grant_revoke_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 0)
        time.sleep(3)

        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(quitledger_result, 0)
        remove_result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(remove_result, 306006)
        grant_result = sub_ledger_node.grantPerm(main_address, chain_admin_private_key)
        assert_code(grant_result, 0)
        grant_result = sub_ledger_node.revokePerm(main_address, chain_admin_private_key)
        assert_code(grant_result, 0)
        time.sleep(2)
        result = sub_ledger_node.remove(another_node_id121, main_private_key)
        assert_code(result, 306006)


    def test_chain_admin_quit_ledger(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey, chain_admin_private_key)
        assert_code(add_result, 0)

        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, chain_admin_private_key)
        assert_code(quitledger_result, 0)
        remove_result = sub_ledger_node.remove(another_node_id121, chain_admin_private_key)
        assert_code(remove_result, 0)



    def test_chain_admin_quit_chaincreator_nopermission_ledger(self, create_ledger_jion_observe_node):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, chain_admin_private_key)
        assert_code(quitledger_result, 0)
        remove_result = sub_ledger_node.remove(another_node_id121, chain_admin_private_key)
        assert_code(remove_result, 306006)


    def test_chain_admin_quit_chaincreator_authorized_ledger(self, create_ledger_jion_observe_node):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, chain_admin_private_key)
        assert_code(quitledger_result, 0)
        remove_result = sub_ledger_node.remove(another_node_id121, chain_admin_private_key)
        assert_code(remove_result, 306006)
        result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        print(result)
        time.sleep(5)
        result = sub_ledger_node.remove(another_node_id121, chain_admin_private_key)
        assert_code(result, 0)


    def test_chain_admin_quit_chaincreator_grant_revoke_ledger(self, create_ledger_jion_observe_node):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, chain_admin_private_key)
        assert_code(quitledger_result, 0)
        remove_result = sub_ledger_node.remove(another_node_id121, chain_admin_private_key)
        assert_code(remove_result, 306006)
        result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        print(result)
        result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        print(result)
        time.sleep(2)
        result = sub_ledger_node.remove(another_node_id121, chain_admin_private_key)
        assert_code(result, 306006)


    @pytest.mark.parametrize('sign_user', [node_admin_private_key, contract_admin_private_key, contract_deployer_private_key, visitor_private_key])
    def test_nopermission_quit_ledger(self, create_ledger_jion_observe_node, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        quitledger_result = ledger.quitLedger(ledger_name, another_node_id121, sign_user)
        assert_code(quitledger_result, 305003)
        remove_result = sub_ledger_node.remove(another_node_id121, sign_user)
        assert_code(remove_result, 306006)




class TestTerminateLedger():


    def test_chaincreator_terminate_chainadmin_create_ledger(self, chainadmin_create_ledger):
        ledger_name, _ = chainadmin_create_ledger
        result = ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)


    def test_terminateLedger(self, create_ledger_jion_observe_node):
        ledger_name, _ = create_ledger_jion_observe_node
        result = ledger.terminateLedger(ledger_name, chain_admin_private_key)
        assert_code(result, 0)


    def test_chain_admin_terminate_ledger(self, chainadmin_create_ledger):
        ledger_name, _ = chainadmin_create_ledger
        result = ledger.terminateLedger(ledger_name, chain_admin_private_key)
        assert_code(result, 0)


    def test_chain_admin_terminate_chaincreator_nopermission_ledger(self, create_ledger):
        ledger_name, _ = create_ledger
        result = ledger.terminateLedger(ledger_name, chain_admin_private_key)
        assert_code(result, 0)


    @pytest.mark.parametrize('sign_user', [node_admin_private_key, contract_admin_private_key, contract_deployer_private_key, visitor_private_key])
    def test_nopermission_quit_ledger(self, create_ledger_jion_observe_node, sign_user):
        ledger_name, _ = create_ledger_jion_observe_node
        result = ledger.terminateLedger(ledger_name, sign_user)
        assert_code(result, 305003)



    @pytest.mark.parametrize('grant_address, sign_user',
                             [(node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_grant_terminateLedger_ledger(self, create_ledger, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)
        result = ledger.terminateLedger(ledger_name, sign_user)
        assert_code(result, 305003)


class TestJoinLedgers():


    def test_joinedledgers(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(5)
        ledger_list = ledger.joinedLedgers(root_node_id)
        ledger_name_list = json.loads(ledger_list[0])['data']
        assert ledger_name in ledger_name_list


    def test_another_node_joinedledgers(self, create_ledger_jion_observe_node):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        time.sleep(5)
        ledger_list = ledger.joinedLedgers(another_node_id121)
        ledger_name_list = json.loads(ledger_list[0])['data']
        assert ledger_name in ledger_name_list


class TestAddNode():

    @pytest.mark.parametrize('sign_user', [chain_admin_private_key, node_admin_private_key, contract_admin_private_key, contract_deployer_private_key, visitor_private_key])
    def test_nopermission_add_node(self, create_ledger, sign_user):
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, sign_user)
        assert_code(add_result, 306006)



    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_authorized_add_node(self, create_ledger, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, sign_user)
        assert_code(add_result, 0)


    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_grant_revke_add_node(self, create_ledger, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id, another_node_bls_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        grant_result = sub_ledger_node.revokePerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)
        add_result = sub_ledger_node.add(another_node_id, another_node_bls_pubkey, sign_user)
        assert_code(add_result, 306006)



class TestRemoveNode():


    @pytest.mark.parametrize('sign_user', [chain_admin_private_key, node_admin_private_key, contract_admin_private_key, contract_deployer_private_key, visitor_private_key])
    def test_nopermission_remove_node(self, create_ledger_jion_observe_node, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        quit_result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(quit_result, 0)
        time.sleep(3)

        remove_result = sub_ledger_node.remove(another_node_id121, sign_user)
        assert_code(remove_result, 306006)



    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_authorized_remove_node(self, create_ledger_jion_observe_node, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        quit_result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(quit_result, 0)
        time.sleep(3)

        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)

        remove_result = sub_ledger_node.remove(another_node_id121, sign_user)
        assert_code(remove_result, 0)


    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_grant_revoke_remove_node(self, create_ledger_jion_observe_node, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        quit_result = ledger.quitLedger(ledger_name, another_node_id121, main_private_key)
        assert_code(quit_result, 0)
        time.sleep(3)

        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        grant_result = sub_ledger_node.revokePerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)

        remove_result = sub_ledger_node.remove(another_node_id121, sign_user)
        assert_code(remove_result, 306006)



class TestUpdateNodeType():


    def test_chainadmin_updatenodetype(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        join_result = ledger.joinLedger(ledger_name, another_node_id121, another_node_bls_pubkey121, chain_admin_private_key)
        assert_code(join_result, 0)
        add_result = sub_ledger_node.add(another_node_id121, another_node_bls_pubkey121, chain_admin_private_key)
        assert_code(add_result, 0)

        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == another_node_id121
        result = sub_ledger_node.updateNodeType(another_node_id121, 1, chain_admin_private_key)
        assert_code(result, 0)
        consensus_node_list = [json.loads(sub_ledger_node.list()[0])['data']['consensus'][i]['nodeID'] for i in range(len(json.loads(sub_ledger_node.list()[0])['data']['consensus']))]
        assert another_node_id121 in consensus_node_list



    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_authorized_updatenodetype(self, create_ledger_jion_observe_node, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == another_node_id121

        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)

        result = sub_ledger_node.updateNodeType(another_node_id121, 1, sign_user)
        assert_code(result, 0)
        time.sleep(5)
        consensus_node_list = [json.loads(sub_ledger_node.list()[0])['data']['consensus'][i]['nodeID'] for i in range(len(json.loads(sub_ledger_node.list()[0])['data']['consensus']))]
        assert another_node_id121 in consensus_node_list



    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_grant_revoke_updatenodetype(self, create_ledger_jion_observe_node, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == another_node_id121

        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        revokePerm_result = sub_ledger_node.revokePerm(grant_address, main_private_key)
        assert_code(revokePerm_result, 0)
        time.sleep(2)
        result = sub_ledger_node.updateNodeType(another_node_id121, 1, sign_user)
        assert_code(result, 306006)



    @pytest.mark.parametrize('sign_user', [chain_admin_private_key, node_admin_private_key, contract_admin_private_key,
                                           contract_deployer_private_key, visitor_private_key])
    def test_nopermission_remove_node(self, create_ledger_jion_observe_node, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == another_node_id121

        result = sub_ledger_node.updateNodeType(another_node_id121, 1, sign_user)
        assert_code(result, 306006)
        time.sleep(5)
        consensus_node_list = [json.loads(sub_ledger_node.list()[0])['data']['consensus'][i]['nodeID'] for i in range(len(json.loads(sub_ledger_node.list()[0])['data']['consensus']))]
        assert another_node_id121 not in consensus_node_list
        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == another_node_id121



class TestGrantPermRrevokePerm():


    def test_grantperm(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)


    def test_chainadmin_granterm(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, chain_admin_private_key)
        assert_code(grantperm_result, 0)


    def test_chainadmin_create_chaincreator_granterm(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 306006)



    @pytest.mark.parametrize('sign_user', [chain_admin_private_key, node_admin_private_key, contract_admin_private_key,
                                           contract_deployer_private_key, visitor_private_key])
    def test_nopermission_grantperm(self, create_ledger, sign_user):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, sign_user)
        assert_code(grantperm_result, 306006)



    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_grant_grantperm(self, create_ledger_jion_observe_node, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        time.sleep(3)
        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, sign_user)
        assert_code(grantperm_result, 306006)



    def test_revokePerm(self, create_ledger):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(result, 0)


    def test_chainadmin_revokePerm(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        time.sleep(3)
        result = sub_ledger_node.revokePerm(node_admin_address, chain_admin_private_key)
        assert_code(result, 0)


    def test_chainadmin_create_chaincreator_revokePerm(self, chainadmin_create_ledger):
        ledger_name, sub_ledger_node = chainadmin_create_ledger
        time.sleep(3)
        result = sub_ledger_node.revokePerm(node_admin_address, main_private_key)
        assert_code(result, 306006)


    @pytest.mark.parametrize('sign_user', [chain_admin_private_key, node_admin_private_key, contract_admin_private_key,
                                           contract_deployer_private_key, visitor_private_key])
    def test_nopermission_revokePerm(self, create_ledger, sign_user):
        ledger_name, sub_ledger_node = create_ledger
        time.sleep(3)
        result = sub_ledger_node.revokePerm(chain_admin_address, sign_user)
        assert_code(result, 306006)


    @pytest.mark.parametrize('grant_address, sign_user',
                             [(chain_admin_address, chain_admin_private_key),
                              (node_admin_address, node_admin_private_key),
                              (contract_admin_address, contract_admin_private_key),
                              (contract_deployer_address, contract_deployer_private_key),
                              (visitor_address, visitor_private_key)])
    def test_grant_revokePerm(self, create_ledger_jion_observe_node, grant_address, sign_user):
        ledger_name, sub_ledger_node = create_ledger_jion_observe_node
        time.sleep(3)
        grant_result = sub_ledger_node.grantPerm(grant_address, main_private_key)
        assert_code(grant_result, 0)
        time.sleep(5)
        result = sub_ledger_node.revokePerm(chain_admin_address, sign_user)
        assert_code(result, 306006)
from cases.ledger.conftest import *




class TestCreatLedger():

    def test_create_ledger(self, clients):
        for client in clients:
            print(client.url)
            print(f'4  listall={client.node.listAll()}')
            ledger_name, sub_ledger_node = create_oneledger(client)
            time.sleep(5)
            print(f'5  listall={client.node.listAll()}')
            len_list = len(json.loads(client.ledger.getAllLedgers()[0])['data'])
            for i in range(len_list):
                if ledger_name == json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                    assert json.loads(client.ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][0]['blsPubKey'] == client.node_pubkey
                    break
            else:
                assert 1 == 2, 'Failed to create ledger'

            # client.ledger.terminateLedger(ledger_name, main_private_key)
            time.sleep(5)



    def test_create_ledger_observer_node(self, rand_client):
        client = rand_client
        time.sleep(5)
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        id = client.node_id
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
                {
                    "PublicKey": id,
                    "nodeType": 2
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 305010)


    def test_create_ledger_same_name(self, client):
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
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
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 305004)

        client.ledger.terminateLedger(ledger_name, main_private_key)


    def test_create_ledger_same_node(self, clients):
        client = clients[7]
        time.sleep(3)
        ledger_name, sub_ledger_node = create_oneledger(client)
        ledger_name2, sub_ledger_node2 = create_oneledger(client)
        len_list = len(json.loads(client.ledger.getAllLedgers()[0])['data'])
        for i in range(len_list):
            if ledger_name2 == json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                assert json.loads(client.ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][0][
                           'blsPubKey'] == client.node_pubkey
                break
        else:
            assert 1 == 2, 'Failed to create ledger'

        client.ledger.terminateLedger(ledger_name, main_private_key)
        client.ledger.terminateLedger(ledger_name2, main_private_key)



    def test_create_ledger_nonexistent_node(self, client):
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
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
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 305009)


    def test_create_ledger_nonode_specified(self, client):
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
                {
                    # "PublicKey": id,
                    # "nodeType": 1
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 305007)


    def test_create_ledger_several_node(self, create_ledger_four_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another, client_another2, client_another3 = clients[1], clients[4], clients[5]
        add_nodes_list = [client.node_pubkey, client_another.node_pubkey, client_another2.node_pubkey, client_another3.node_pubkey]
        len_list = len(json.loads(client.ledger.getAllLedgers()[0])['data'])
        for i in range(len_list):
            if ledger_name == json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                len_consensus_nodes = len(json.loads(client.ledger.getAllLedgers()[0])['data'][i]['consensusNodes'])
                for j in range(len_consensus_nodes):
                    node_blspubkey = json.loads(client.ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][j]['blsPubKey']
                    if node_blspubkey in add_nodes_list:
                        add_nodes_list.remove(node_blspubkey)
                assert len(add_nodes_list) == 0
                break
        else:
            assert 1 == 2, 'Failed to create ledger'



    def test_create_ledger_several_observe_node(self, clients):
        client, client1, client2 = clients[0], clients[1], clients[4]
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
                {
                    "PublicKey": client.node_id,
                    "nodeType": 2
                },
                {
                    "PublicKey": client1.node_id,
                    "nodeType": 2
                },
                {
                    "PublicKey": client2.node_id,
                    "nodeType": 2
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 305010)


    def test_create_ledger_several_same_node(self, create_two_ledger):
        ledger_name_list, sub_ledger_node_list, client = create_two_ledger
        len_list = len(json.loads(client.ledger.getAllLedgers()[0])['data'])
        for i in range(len_list):
            if ledger_name_list[0] == json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                assert json.loads(client.ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][0][
                           'blsPubKey'] == client.node_pubkey
                break
        else:
            assert 1 == 2, 'Failed to create ledger'


    @pytest.mark.parametrize('nodetype', [1, 2])
    def test_create_ledger_several_nonexistent_node(self, nodetype, clients):
        client, client1, client2 = clients[0], clients[1], clients[5]
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
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
                    "PublicKey": nonexistent_node_id,
                    "nodeType": nodetype
                },
                {
                    "PublicKey": client1.node_id,
                    "nodeType": 1
                },
                {
                    "PublicKey": client2.node_id,
                    "nodeType": 1
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 305009)


    def test_create_ledger_oneconsensus_node(self, clients):
        client, client1, client2, client3 = clients[0], clients[1], clients[5], clients[6]
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        ledger_name = "test" + str(nonce)
        id = client.node_id
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
                {
                    "PublicKey": id,
                    "nodeType": 2
                },
                {
                    "PublicKey": client1.node_id,
                    "nodeType": 2
                },
                {
                    "PublicKey": client2.node_id,
                    "nodeType": 2
                },
                {
                    "PublicKey": client3.node_id,
                    "nodeType": 1
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 0)
        len_list = len(json.loads(client.ledger.getAllLedgers()[0])['data'])
        observernodes_blspubkey_list = [client.node_pubkey, client1.node_pubkey, client2.node_pubkey]
        for i in range(len_list):
            if ledger_name == json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                assert json.loads(client.ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][0][
                           'blsPubKey'] == client3.node_pubkey
                len_observer_nodes = len(json.loads(client.ledger.getAllLedgers()[0])['data'][i]['observerNodes'])
                for j in range(len_observer_nodes):
                    observernode_blspubkey = json.loads(client.ledger.getAllLedgers()[0])['data'][i]['observerNodes'][j]['blsPubKey']
                    if observernode_blspubkey in observernodes_blspubkey_list:
                        observernodes_blspubkey_list.remove(observernode_blspubkey)
                assert len(observernodes_blspubkey_list) == 0

        client.ledger.terminateLedger(ledger_name, main_private_key)


    def test_terminate_ledger_create_same_name_ledger(self, create_ledger, clients):
        ledger_name, sub_ledger_node, client = create_ledger
        another_client = clients[4]
        result = client.ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        time.sleep(3)

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
        assert_code(result, 305004)



class TestJoinLedger():

    def test_join_ledger(self, create_ledger_jion_observe_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        observe_client_another = clients[4]
        jion_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert jion_nodeid == observe_client_another.node_id
        assert_blocknumber_growth(sys_ledger, ledger_name, client)



    def test_join_ledger_observer(self, create_ledger, clients):
        ledger_name, sub_ledger_node, client = create_ledger
        client_another = clients[4]
        join_result = client.ledger.joinLedger(ledger_name, client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(add_result, 0)
        jion_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert jion_nodeid == client_another.node_id


    def test_join_ledger_nonexistent_node(self, create_ledger):
        # 子帐本add的时候不会判断节点是不是存在链上，所以可以add成功，但是join不会成功
        ledger_name, sub_ledger_node, client = create_ledger
        join_result = client.ledger.joinLedger(ledger_name, nonexistent_node_id, nonexistent_node_bls_pubkey, main_private_key)
        assert_code(join_result, 301019)
        time.sleep(3)
        add_result = sub_ledger_node.add(nonexistent_node_id, nonexistent_node_bls_pubkey, main_private_key)
        assert_code(add_result, 0)


    def test_join_nonexistent_ledger(self, clients):
        client, client_another = clients[0], clients[4]
        ledger_name = 'xxxxxxxx'
        join_result = client.ledger.joinLedger(ledger_name, client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(join_result, 305005)
        time.sleep(3)
        sub_ledger_node = ledger_node.LedgerNode(client_another.web3, ledger_name)
        sub_ledger_node.is_wait_receipt = True
        status = True
        try:
            add_result = sub_ledger_node.add(client_another.node_id, client_another.node_pubkey, main_private_key)
        except:
            status = False
        assert status == False



    def test_join_ledger_repeat(self, create_ledger_jion_consensus_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_consensus_node
        client_another = clients[1]
        join_result = client.ledger.joinLedger(ledger_name, client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(join_result, 305013)
        add_result = sub_ledger_node.add(client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(add_result, 306012)



class TestQuitLedger():

    def test_quit_ledger(self, create_ledger_jion_observe_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        observe_client_another = clients[4]
        result = client.ledger.quitLedger(ledger_name, observe_client_another.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(observe_client_another.node_id, main_private_key)
        assert_code(result, 0)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)
        sub_observernode_list = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert sub_observernode_list == []

        join_result = client.ledger.joinLedger(ledger_name, observe_client_another.node_id, observe_client_another.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        add_result = sub_ledger_node.add(observe_client_another.node_id, observe_client_another.node_pubkey, main_private_key)
        assert_code(add_result, 0)

        time.sleep(15)
        sub_observernode_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert sub_observernode_nodeid == observe_client_another.node_id




    def test_quit_nonexistent_ledger(self, create_ledger_jion_observe_node, clients):
        client, client_another = clients[0], clients[4]
        ledger_name = 'xxxxxxx'
        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 305005)
        sub_ledger_node = ledger_node.LedgerNode(client.web3, ledger_name)
        sub_ledger_node.is_wait_receipt = True
        status = True
        try:
            result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        except:
            status = False
        assert status == False



    def test_quit_ledger_nonexistent_node(self, create_ledger_jion_observe_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        client_another = clients[5]
        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 305014)
        result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(result, 306008)


    def test_quit_ledger_repeat(self, create_ledger_jion_observe_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        client_another = clients[4]
        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(result, 0)

        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 305014)
        result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(result, 306008)


    def test_quit_ledger_consensus(self, create_ledger_two_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_two_node
        client_another = clients[1]
        time.sleep(5)
        result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(result, 306007)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 0)
        status = False
        try:
            result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        except:
            status = True
        assert  status
        sub_blocknumber = client.platone.blockNumber(ledger_name)
        time.sleep(3)
        sub_blocknumber_wait = client.platone.blockNumber(ledger_name)
        assert sub_blocknumber_wait == sub_blocknumber



    def test_quit_ledger_consensus_to_observer(self, create_ledger_four_node, clients):
        #todo: 为什么等一个结算周期不行要等两个呢？
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another = clients[1]
        time.sleep(5)
        result = sub_ledger_node.updateNodeType(client_another.node_id, 2, main_private_key)
        assert_code(result, 0)
        wait_settlement(client.platone, settlement=1)
        time.sleep(10)
        node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert node_id == client_another.node_id
        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(result, 0)
        observer_list = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert observer_list == []



    def test_quit_ledger_consensus_to_observer_not_effective(self, create_ledger_four_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another = clients[1]
        time.sleep(3)
        update_result = sub_ledger_node.updateNodeType(client_another.node_id, 2, main_private_key)
        assert_code(update_result, 0)
        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 0)
        remove_result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(remove_result, 306007)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)




class TestTerminateLedger():

    def test_terminate_ledger(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        ledger = client.ledger
        time.sleep(3)
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

        assert_sys_blocknumber_growth_sub_notgrowth(sys_ledger, ledger_name, client)



    def test_terminate_ledger_several_node(self, create_ledger_four_node):
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        time.sleep(3)
        ledger_list = [json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName'] for i in range(len(json.loads(client.ledger.getAllLedgers()[0])['data']))]
        assert ledger_name in ledger_list

        result = client.ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        ledger_list = [json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName'] for i in range(len(json.loads(client.ledger.getAllLedgers()[0])['data']))]
        assert ledger_list == []
        status = False
        try:
            result = sub_ledger_node.list()
        except:
            status = True
        assert status


    def test_terminate_ledger_nonexistent(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        nonexistent_ledger_name = 'xxxxxxx'
        result = client.ledger.terminateLedger(nonexistent_ledger_name, main_private_key)
        assert_code(result, 305005)


    def test_terminate_ledger_repeat(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        result = client.ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        repeat_result = client.ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(repeat_result, 305017)


    def test_terminate_repeatedly(self, client):
        for i in range(10):
            ledger_name, _ = create_oneledger(client)
            print(f'i: ledger_name: {i, ledger_name}')
            time.sleep(2)
            result = client.ledger.terminateLedger(ledger_name, main_private_key)
            assert_code(result, 0)

            assert_sys_blocknumber_growth_sub_notgrowth(sys_ledger, ledger_name, client)



class TestUpdateNodeType():


    def test_updatenodetype(self, create_ledger_jion_observe_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        observe_client_another = clients[4]
        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == observe_client_another.node_id
        result = sub_ledger_node.updateNodeType(observe_client_another.node_id, 1, main_private_key)
        assert_code(result, 0)
        consensus_node_list = [json.loads(sub_ledger_node.list()[0])['data']['consensus'][i]['nodeID'] for i in range(len(json.loads(sub_ledger_node.list()[0])['data']['consensus']))]
        assert observe_client_another.node_id in consensus_node_list
        assert_blocknumber_growth(sys_ledger, ledger_name, client)


    def test_updatenodetype_con_to_obs(self, create_ledger_four_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another = clients[4]
        time.sleep(5)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []
        result = sub_ledger_node.updateNodeType(client_another.node_id, 2, main_private_key)
        assert_code(result, 0)
        update_obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert update_obs_nodeid == client_another.node_id



    def test_updatenodetype_con_to_obs_border(self, create_ledger_three_node, clients):
        # todo: 还是有那个编码问题
        ledger_node, sub_ledger_node, client = create_ledger_three_node
        client_another = clients[4]
        time.sleep(3)
        nodes_info = json.loads(sub_ledger_node.list()[0])
        obs_nodeid = nodes_info['data']['observer']
        assert obs_nodeid == []
        result = sub_ledger_node.updateNodeType(client_another.node_id, 2, main_private_key)
        assert_code(result, 0)
        time.sleep(3)
        nodes_info = json.loads(sub_ledger_node.list()[0])
        update_obs_nodeid = nodes_info['data']['observer'][0]['nodeID']
        assert update_obs_nodeid == client_another.node_id



    def test_updateNodeType_con_to_obs_less(self, create_ledger_two_node, clients):
        """
        todo: 不能低于共识列表的2/3限制只在ptool管理台做了限制
        """
        ledger_name, sub_ledger_node, client = create_ledger_two_node
        client_another = clients[1]
        time.sleep(10)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []

        result = sub_ledger_node.updateNodeType(client_another.node_id, 2, main_private_key)
        assert_code(result, 0)

        sub_ledger_list = sub_ledger_node.list()
        update_obs_nodeid = json.loads(sub_ledger_list[0])['data']['observer'][0]['nodeID']
        assert update_obs_nodeid == client_another.node_id



    def test_updatenodetype_onlycon_to_obs(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        time.sleep(10)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []
        result = sub_ledger_node.updateNodeType(client.node_id, 2, main_private_key)
        assert_code(result, 306011)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []


    def test_updatenodetype_obs_to_obs(self, create_ledger_jion_observe_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        observe_client_another = clients[4]
        time.sleep(3)
        observer_node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == observe_client_another.node_id
        result = sub_ledger_node.updateNodeType(observe_client_another.node_id, 2, main_private_key)
        assert_code(result, 0)
        time.sleep(3)
        observer_node_id_update = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id == observer_node_id_update
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        wait_settlement(client.platone)
        observer_node_id_update_waitseetlement = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id_update == observer_node_id_update_waitseetlement
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        wait_settlement(client.platone)
        observer_node_id_update_waitseetlement = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert observer_node_id_update == observer_node_id_update_waitseetlement
        assert_blocknumber_growth(sys_ledger, ledger_name, client)


    def test_updatenodetype_con_to_con(self, create_ledger):
        # bug19527已验证
        ledger_name, sub_ledger_node, client = create_ledger
        time.sleep(3)
        consensus_node_id = json.loads(sub_ledger_node.list()[0])['data']['consensus'][0]['nodeID']
        assert consensus_node_id == client.node_id
        result = sub_ledger_node.updateNodeType(client.node_id, 1, main_private_key)
        assert_code(result, 0)
        time.sleep(3)
        consensus_node_id_update = json.loads(sub_ledger_node.list()[0])['data']['consensus'][0]['nodeID']
        assert consensus_node_id == consensus_node_id_update
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        wait_settlement(client.platone)
        consensus_node_id_update_waitseetlement = json.loads(sub_ledger_node.list()[0])['data']['consensus'][0]['nodeID']
        assert consensus_node_id_update == consensus_node_id_update_waitseetlement
        assert_blocknumber_growth(sys_ledger, ledger_name, client)



class TestJoinLedgers():


    def test_joinedledgers(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        time.sleep(5)
        ledger_list = client.ledger.joinLedgers(client.node_id)
        ledger_name_list = json.loads(ledger_list[0])['data']
        assert ledger_name in ledger_name_list


    # @pytest.mark.parametrize('ledger_node', [ledger, ledger_122, ledger_123, ledger_124, ledger_anther, ledger_anther122, ledger_anther123, ledger_anther124])
    def test_another_node_joinedledgers(self, create_ledger_jion_observe_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        observe_client_another = clients[4]
        time.sleep(5)
        for client in clients:
            ledger_list = client.ledger.joinLedgers(observe_client_another.node_id)
            ledger_name_list = json.loads(ledger_list[0])['data']
            assert ledger_name in ledger_name_list


    def test_nonexistent_node_joinedledgers(self, client):
        ledger_list = client.ledger.joinLedgers(nonexistent_node_id)
        assert json.loads(ledger_list[0])['data'] == []




class TestGrantRrevokePerm():

    def test_grantperm(self, create_ledger):
        ledger_name, sub_ledger_node, _ = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)

    def test_grantperm_repeat(self, create_ledger):
        ledger_name, sub_ledger_node, _ = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)
        time.sleep(3)
        # 这里底层需不需要改？前端更改了没有验证
        repeat_grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(repeat_grantperm_result, 0)


    def test_revokeperm(self, create_ledger):
        ledger_name, sub_ledger_node, _ = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)
        time.sleep(3)
        grantperm_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)


    def test_nogrant_revokeperm(self, create_ledger):
        ledger_name, sub_ledger_node, _ = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)


    def test_revokeperm_repeat(self, create_ledger):
        ledger_name, sub_ledger_node, _ = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)
        time.sleep(3)
        revoke_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(revoke_result, 0)
        time.sleep(3)
        repeat_revoke_result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(repeat_revoke_result, 0)

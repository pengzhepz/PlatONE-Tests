from cases.ledger.conftest import *




class TestInformationStorage():


    def test_information_storage_nonsubledger_node(self, create_ledger, clients):
        ledger_name, sub_ledger_node, client = create_ledger
        client_another = clients[4]
        time.sleep(5)
        node_list = sub_ledger_node.list()
        assert_code(json.loads(node_list[0]), 0)
        nonsub_ledger_node = ledger_node.LedgerNode(client_another.web3, ledger_name)
        nonsub_ledger_node.is_wait_receipt = True
        status = False
        try:
            node_list_nonsub = nonsub_ledger_node.list()
        except:
            status = True
        assert status
        nonsub_ledger_node1 = ledger_node.LedgerNode(client.web3, sys_ledger)
        nonsub_ledger_node1.is_wait_receipt = True
        node_list_nonsub1 = nonsub_ledger_node1.list()
        assert_code(json.loads(node_list_nonsub1[0]), 306001)


    def test_information_storage_subledger_node(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        time.sleep(3)
        node_info = json.loads(sub_ledger_node.list()[0])
        assert_code(node_info, 0)
        node_id = node_info['data']['consensus'][0]['nodeID']
        assert node_id == client.node_id


    def test_information_storage_different_subledgers(self, create_two_ledger):
        ledger_name_list, sub_ledger_node_list, client = create_two_ledger
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name_list[0], client)
        transaction_blocknumber = transaction_receipt['blockNumber']
        transaction_blockhash = transaction_receipt['blockHash']
        transaction_hash = transaction_receipt['transactionHash']
        time.sleep(5)
        prepare = client.platone.getPrepareQC(transaction_blocknumber, ledger_name_list[0])
        prepare1 = client.platone.getPrepareQC(transaction_blocknumber, ledger_name_list[1])
        assert HexBytes(prepare['blockHash']) == transaction_blockhash
        assert prepare['blockNumber'] == transaction_blocknumber
        assert prepare1 is None

        transaction_info = client.platone.getTransaction(transaction_hash.hex(), ledger_name_list[0])
        transaction_info1 = client.platone.getTransaction(transaction_hash.hex(), ledger_name_list[1])
        assert transaction_info1 is None
        assert transaction_info['blockHash'] == transaction_blockhash


    def test_information_storage_same_subledger(self, create_ledger_jion_three_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_three_node
        client_anther, client_anther2, client_anther3 = clients[4], clients[5], clients[1]
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_blocknumber = transaction_receipt['blockNumber']
        transaction_blockhash = transaction_receipt['blockHash']
        transaction_hash = transaction_receipt['transactionHash']
        time.sleep(10)
        prepare = client.platone.getPrepareQC(transaction_blocknumber, ledger_name)
        prepare1 = client_anther.platone.getPrepareQC(transaction_blocknumber, ledger_name)
        prepare2 = client_anther2.platone.getPrepareQC(transaction_blocknumber, ledger_name)
        prepare3 = client_anther3.platone.getPrepareQC(transaction_blocknumber, ledger_name)
        assert prepare['blockHash'] == prepare1['blockHash'] == prepare2['blockHash'] == prepare3['blockHash'] == transaction_blockhash.hex()

        transaction_info = client.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info1 = client_anther.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info2 = client_anther2.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info3 = client_anther3.platone.getTransaction(transaction_hash.hex(), ledger_name)
        assert transaction_info['blockHash'] == transaction_info1['blockHash'] == transaction_info2['blockHash'] == transaction_info3['blockHash'] == transaction_blockhash




class TestInformationClean():


    def test_information_clean_quit_ledger(self, create_ledger_jion_two_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_two_node
        client_anther, client_anther2 = clients[4], clients[1]
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash = transaction_receipt['transactionHash']
        time.sleep(3)
        result = client.ledger.quitLedger(ledger_name, client_anther.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(client_anther.node_id, main_private_key)
        assert_code(result, 0)
        transaction_info = client.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info1 = client_anther.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info2 = client_anther2.platone.getTransaction(transaction_hash.hex(), ledger_name)
        assert transaction_info['blockHash'] == transaction_info2['blockHash'] == transaction_receipt['blockHash']
        assert transaction_info1 is None



    def test_information_clean_terminate_ledger(self, create_ledger_jion_two_node, clients):
        ledger_name, sub_ledger_node, client= create_ledger_jion_two_node
        client_anther, client_anther2 = clients[4], clients[1]
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash = transaction_receipt['transactionHash']
        time.sleep(3)
        result = client.ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        time.sleep(5)
        transaction_info = client.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info1 = client_anther.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info2 = client_anther2.platone.getTransaction(transaction_hash.hex(), ledger_name)
        assert transaction_info2 == transaction_info1 == transaction_info is None



    def test_information_clean_quit_join_ledger(self, create_ledger_jion_two_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_two_node
        client_anther, client_anther2 = clients[4], clients[1]
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash = transaction_receipt['transactionHash']
        time.sleep(3)
        result = client.ledger.quitLedger(ledger_name, client_anther.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(client_anther.node_id, main_private_key)
        assert_code(result, 0)
        time.sleep(20)
        transaction_receipt1 = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash1 = transaction_receipt1['transactionHash']
        wait_settlement(client.platone)
        join_result = client.ledger.joinLedger(ledger_name, client_anther.node_id, client_anther.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(client_anther.node_id, client_anther.node_pubkey, main_private_key)
        assert_code(add_result, 0)

        transaction_info = client_anther.platone.getTransaction(transaction_hash.hex(), ledger_name)
        assert transaction_info['blockHash'] == transaction_receipt['blockHash']
        transaction_info1 = client_anther.platone.getTransaction(transaction_hash1.hex(), ledger_name)
        assert transaction_info1['blockHash'] == transaction_receipt1['blockHash']


    def test_delete_ledger_observer_data(self, create_ledger_jion_two_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_jion_two_node
        client_anther, client_anther2 = clients[4], clients[1]
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash = transaction_receipt['transactionHash']
        global_test_env.clean_subledger(client_anther.url, ledger_name)

        for i in range(5):
            assert_blocknumber_growth(sys_ledger, ledger_name, client)

        transaction_info = client.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info_another = client_anther.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info_anther122 = client_anther2.platone.getTransaction(transaction_hash.hex(), ledger_name)

        assert transaction_info['hash'] == transaction_info_another['hash']  == transaction_info_anther122['hash'] == transaction_hash
        global_test_env.stop_designated_node(client_anther.url)
        time.sleep(3)
        status = False
        try:
            transaction = client_anther.platone.getTransaction(transaction_hash.hex(), ledger_name)
        except:
            status = True
        assert status



    def test_delete_ledger_consensus_data(self, create_ledger_two_node, clients, global_test_env):
        #bug19595 已验。共识节点删除本地数据库后，不杀进程，不影响共识
        ledger_name, sub_ledger_node, client = create_ledger_two_node
        client_another = clients[1]
        time.sleep(3)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash = transaction_receipt['transactionHash']
        time.sleep(3)

        global_test_env.clean_subledger(client_another.url, ledger_name)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)


    def test_quit_ledger_delete_data(self, create_ledger_jion_two_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_jion_two_node
        client_another = clients[4]
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash = transaction_receipt['transactionHash']
        time.sleep(3)
        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(result, 0)

        global_test_env.clean_designated_node(client_another.url, ledger_name)
        time.sleep(3)
        global_test_env.start_designated_node(client_another.url)
        time.sleep(3)

        join_result = client.ledger.joinLedger(ledger_name, client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        add_result = sub_ledger_node.add(client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(add_result, 0)
        time.sleep(30)

        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        transaction_info = client.platone.getTransaction(transaction_hash.hex(), ledger_name)
        transaction_info_122 = client_another.platone.getTransaction(transaction_hash.hex(), ledger_name)
        assert transaction_info_122['hash'] == transaction_info['hash'] == transaction_hash



    def test_delete_terminate_ledger_data(self, create_ledger_jion_two_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_jion_two_node
        client_anther = clients[5]
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        transaction_hash = transaction_receipt['transactionHash']

        result = client.ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)
        time.sleep(10)

        global_test_env.clean_designated_node(client_anther.url, ledger_name)
        time.sleep(5)
        global_test_env.start_designated_node(client_anther.url)
        time.sleep(3)

        transaction_info = client.platone.getTransaction(transaction_hash.hex(), ledger_name)
        assert transaction_info is None
        transaction_info_another_platone = client_anther.platone.getTransaction(transaction_hash.hex(), ledger_name)
        assert transaction_info_another_platone is None



    def test_notdelete_quit_join_ledger(self, create_ledger_jion_two_node, clients):
        ledger_name, sub_ledger_node, client = create_ledger_jion_two_node
        client_anther = clients[4]
        time.sleep(3)
        target_node_blocknumber = client_anther.platone.blockNumber(ledger_name)
        result = client.ledger.quitLedger(ledger_name, client_anther.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(client_anther.node_id, main_private_key)
        assert_code(result, 0)
        wait_settlement(client.platone, ledger_name)
        join_result = client.ledger.joinLedger(ledger_name, client_anther.node_id, client_anther.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(1)
        add_result = sub_ledger_node.add(client_anther.node_id, client_anther.node_pubkey, main_private_key)
        assert_code(add_result, 0)
        target_node_blocknumber_befor = client_anther.platone.blockNumber(ledger_name)
        assert 0 < target_node_blocknumber_befor - target_node_blocknumber
        time.sleep(20)
        blocknumber = client.platone.blockNumber(ledger_name)
        target_node_blocknumber_after = client_anther.platone.blockNumber(ledger_name)
        assert abs(target_node_blocknumber_after - blocknumber) <= 2



    def test_delete_subledger_consensus_anomaly(self, clients, global_test_env):
        #  bug19597
        #  todo: 这个用例需要运行很长一段时间后手动看看节点会不会停掉。如果该节点停掉但是不影响链正常运行，就是正常的。
        client, client1, client2, client3, client4 = clients[0], clients[3], clients[4], clients[5], clients[6]
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
                    "PublicKey": client1.node_id,
                    "nodeType": 1
                },
                {
                    "PublicKey": client2.node_id,
                    "nodeType": 1
                },
                {
                    "PublicKey": client3.node_id,
                    "nodeType": 1
                },
                {
                    "PublicKey": client4.node_id,
                    "nodeType": 2
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 0)
        time.sleep(5)
        for i in range(5):
            transfer(main_private_key, user_address, 1, sys_ledger, client)
            transfer(main_private_key, user_address, 1, ledger_name, client)

        wait_settlement(platone)
        global_test_env.clean_subledger(client1.url, ledger_name)

        time.sleep(5)

        assert_blocknumber_growth(sys_ledger, ledger_name, client1)

        for i in range(20):
            transfer(main_private_key, user_address, 1, sys_ledger, client1)
            transfer(main_private_key, user_address, 1, ledger_name, client1)




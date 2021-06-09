from cases.ledger.conftest import *



class TestEmptyBlockConfiguration():


    def test_produce_empty_block_simultaneous_growth (self, produce_empty_block):
        ledger_name, client = produce_empty_block
        for i in range(5):
            assert_blocknumber_growth(sys_ledger, ledger_name, client)


    def test_notproduce_empty_block(self, not_produce_empty_block):
        ledger_name, client = not_produce_empty_block
        for i in range(5):
            assert_not_produce_empty_block(sys_ledger, ledger_name, client)


    def test_notproduce_empty_block_systransaction(self, not_produce_empty_block):
        ledger_name, client = not_produce_empty_block
        blocknumber = client.platone.blockNumber(sys_ledger)
        blocknumber_subledger = client.platone.blockNumber(ledger_name)
        transaction_receipt = transfer(main_private_key, user_address, 1, sys_ledger, client)
        assert transaction_receipt['status'] == 1
        blocknumber_after = client.platone.blockNumber(sys_ledger)
        sub_blocknumber_after = client.platone.blockNumber(ledger_name)
        assert blocknumber_after - blocknumber == 3 and sub_blocknumber_after == blocknumber_subledger
        time.sleep(10)
        blocknumber_after1 = client.platone.blockNumber(sys_ledger)
        sub_blocknumber_after1 = client.platone.blockNumber(ledger_name)
        assert blocknumber_after1 == blocknumber_after and sub_blocknumber_after1 == sub_blocknumber_after


    def test_notproduce_empty_block_subtransaction(self, not_produce_empty_block):
        ledger_name, client = not_produce_empty_block
        blocknumber = client.platone.blockNumber(sys_ledger)
        blocknumber_subledger = client.platone.blockNumber(ledger_name)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        blocknumber_after = client.platone.blockNumber(sys_ledger)
        sub_blocknumber_after = client.platone.blockNumber(ledger_name)
        assert sub_blocknumber_after - blocknumber_subledger == 3 and blocknumber_after == blocknumber
        time.sleep(10)
        blocknumber_after1 = client.platone.blockNumber(sys_ledger)
        sub_blocknumber_after1 = client.platone.blockNumber(ledger_name)
        assert blocknumber_after1 == blocknumber_after and sub_blocknumber_after1 == sub_blocknumber_after




    def test_notproduce_empty_block_createsubledger(self, not_produce_empty_block):
        ledger_name, client = not_produce_empty_block
        sys_blocknumber = client.platone.blockNumber(sys_ledger)
        new_ledger_name, _ = create_oneledger(client)
        for i in range(3):
            blocknumber = client.platone.blockNumber(new_ledger_name)
            sys_blocknumber_after = client.platone.blockNumber(sys_ledger)
            assert sys_blocknumber_after - sys_blocknumber == 3
            time.sleep(3)
            blocknumber1 = client.platone.blockNumber(new_ledger_name)
            sys_blocknumber_after1 = client.platone.blockNumber(sys_ledger)
            assert blocknumber1 == blocknumber == 0 and sys_blocknumber_after == sys_blocknumber_after1


    def test_notproduce_empty_block_createsubledger_transaction(self, not_produce_empty_block):
        # bug19523已验证通过
        ledger_name, client = not_produce_empty_block
        platone = client.platone
        sys_blocknumber = client.platone.blockNumber(sys_ledger)
        new_ledger_name, _ = create_oneledger(client)
        time.sleep(2)
        transaction_receipt = transfer(main_private_key, user_address, 1, new_ledger_name, client)
        print(transaction_receipt)
        for i in range(3):
            blocknumber = platone.blockNumber(new_ledger_name)
            sys_blocknumber_after = platone.blockNumber(sys_ledger)
            assert sys_blocknumber_after - sys_blocknumber == 3
            time.sleep(10)
            blocknumber1 = platone.blockNumber(new_ledger_name)
            sys_blocknumber_after1 = platone.blockNumber(sys_ledger)
            assert blocknumber == blocknumber1 == 1 and sys_blocknumber_after == sys_blocknumber_after1



    def test_notproduce_empty_block_observer_transaction(self, create_ledger_four_node, clients):
        # bug19574已验证通过
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another = clients[7]
        update_result = client.param.updateIsProduceEmptyBlock(False, main_private_key)
        assert_code(update_result, 0)
        join_result = client.ledger.joinLedger(ledger_name, client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(10)
        add_result = sub_ledger_node.add(client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(add_result, 0)
        time.sleep(3)
        result = transfer(main_private_key, user_address, 1, ledger_name, client_another)
        assert result['status'] == 1
        status = client.txpool.status(ledger_name)
        assert status['pending'] == status['queued'] == '0x0'

        update_result = client.param.updateIsProduceEmptyBlock(True, main_private_key)
        assert_code(update_result, 0)




class TestNodeAbnormal():

    def test_sysobserver_node_abnormal_notaffect_subledger(self, create_ledger_jion_observe_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        client_anther = clients[4]
        global_test_env.stop_designated_node(client_anther.url)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        global_test_env.start_designated_node(client_anther.url)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)


    def test_sysobserver_node_abnormal_affect_subledger(self, clients, global_test_env):
        client, client_anther = clients[0], clients[4]
        ledger_name, sub_ledger_node, _ = create_twonodes_ledger(client, client_anther)
        time.sleep(10)
        global_test_env.stop_designated_node(client_anther.url)
        for i in range(5):
            assert_sys_blocknumber_growth_sub_notgrowth(sys_ledger, ledger_name, client)

        global_test_env.start_designated_node(client_anther.url)
        sub_blocknumbe = client.platone.blockNumber(ledger_name)
        time.sleep(30)
        sub_blocknumber_wait = client.platone.blockNumber(ledger_name)
        assert 0 < sub_blocknumber_wait - sub_blocknumbe



    def test_sysobserver_node_abnormal_affect_subledger_wait_settlement(self, clients, global_test_env):
        client, client_anther = clients[0], clients[4]
        ledger_name, sub_ledger_node, client = create_twonodes_ledger(client, client_anther)
        time.sleep(5)
        global_test_env.stop_designated_node(client_anther.url)
        assert_sys_blocknumber_growth_sub_notgrowth(sys_ledger, ledger_name, client)

        wait_settlement(client.platone, settlement=1)
        global_test_env.start_designated_node(client_anther.url)

        time.sleep(30)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)



    def test_sysconsensus_node_abnormal_notaffect_subledger(self, clients, global_test_env):
        client = clients[0]
        node_list = client.node.listAll()
        data = json.loads(node_list[0])['data']
        node_name_list = [data[i]['name'] for i in range(len(data))]
        need_update_nodelist = [name for name in node_name_list if name[-4:] == '7789']
        for name in need_update_nodelist:
            result = client.node.updateType(name, 2, main_private_key)
            assert_code(result, 0)
        for i in range(len(clients)):
            if clients[i].url == 'http://192.168.16.121:7789':
                sys_consensus_client, client_another = clients[i], clients[i + 1]
        time.sleep(20)
        ledger_name, sub_ledger_node = create_oneledger(client_another)
        join_result = client.ledger.joinLedger(ledger_name, client.node_id, client.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(client.node_id, client.node_pubkey, main_private_key)
        assert_code(add_result, 0)

        time.sleep(10)
        global_test_env.stop_designated_node(sys_consensus_client.url)
        for i in range(5):
            assert_sys_blocknumber_notgrowth_sub_growth(sys_ledger, ledger_name, client_another)

        global_test_env.start_designated_node(client.url)
        time.sleep(30)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        sys_updatenodetype(client)
        client_another.ledger.terminateLedger(ledger_name, main_private_key)



    def test_sysconsensus_node_abnormal_notaffect_subledger_wait_settlement(self, clients, global_test_env):
        client = clients[0]
        node_list = client.node.listAll()
        data = json.loads(node_list[0])['data']
        node_name_list = [data[i]['name'] for i in range(len(data))]
        need_update_nodelist = [name for name in node_name_list if name[-4:] == '7789']
        for name in need_update_nodelist:
            result = client.node.updateType(name, 2, main_private_key)
            assert_code(result, 0)
        for i in range(len(clients)):
            if clients[i].url == 'http://192.168.16.121:7789':
                sys_consensus_client, client_another = clients[i], clients[i + 1]
        time.sleep(20)
        ledger_name, sub_ledger_node = create_oneledger(client_another)
        join_result = client.ledger.joinLedger(ledger_name, client.node_id, client.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(client.node_id, client.node_pubkey, main_private_key)
        assert_code(add_result, 0)
        time.sleep(10)
        global_test_env.stop_designated_node(sys_consensus_client.url)
        for i in range(5):
            assert_sys_blocknumber_notgrowth_sub_growth(sys_ledger, ledger_name, client_another)
        wait_settlement(client_another.platone, ledger=ledger_name, settlement=1)
        global_test_env.start_designated_node(client.url)
        time.sleep(30)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        sys_updatenodetype(client)
        client_another.ledger.terminateLedger(ledger_name, main_private_key)





    def test_sysconsensus_node_abnormal_taffect_subledger(self, clients, global_test_env):
        client = clients[0]
        node_list = client.node.listAll()
        data = json.loads(node_list[0])['data']
        node_name_list = [data[i]['name'] for i in range(len(data))]
        need_update_nodelist = [name for name in node_name_list if name[-4:] == '7789']
        for name in need_update_nodelist:
            result = client.node.updateType(name, 2, main_private_key)
            assert_code(result, 0)
        for i in range(len(clients)):
            if clients[i].url == 'http://192.168.16.121:7789':
                sys_consensus_client, client_another = clients[i], clients[i + 1]
        time.sleep(20)
        ledger_name, sub_ledger_node, _ = create_twonodes_ledger(sys_consensus_client, client_another)
        time.sleep(10)
        global_test_env.stop_designated_node(sys_consensus_client.url)
        time.sleep(10)
        for i in range(5):
            assert_sys_sub_blocknumber_notgrowth(sys_ledger, ledger_name, client_another)

        global_test_env.start_designated_node(sys_consensus_client.url)
        time.sleep(30)
        assert_blocknumber_growth(sys_ledger, ledger_name, client_another)

        sys_updatenodetype(client)
        client_another.ledger.terminateLedger(ledger_name, main_private_key)



    def test_sysconsensus_node_abnormal_taffect_subledger_wait_settlement(self, clients, global_test_env):
        client = clients[0]
        node_list = client.node.listAll()
        data = json.loads(node_list[0])['data']
        node_name_list = [data[i]['name'] for i in range(len(data))]
        need_update_nodelist = [name for name in node_name_list if name[-4:] == '7789']
        for name in need_update_nodelist:
            result = client.node.updateType(name, 2, main_private_key)
            assert_code(result, 0)
        for i in range(len(clients)):
            if clients[i].url == 'http://192.168.16.121:7789':
                sys_consensus_client, client_another = clients[i], clients[i + 1]
        time.sleep(20)
        ledger_name, sub_ledger_node = create_twonodes_ledger(sys_consensus_client, client_another)
        time.sleep(10)

        wait_settlement(client.platone, sys_ledger, settlement=1)
        global_test_env.stop_designated_node(sys_consensus_client.url)
        for i in range(5):
            assert_sys_sub_blocknumber_notgrowth(sys_ledger, ledger_name, client_another)

        global_test_env.start_designated_node(sys_consensus_client.url)
        time.sleep(30)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        sys_updatenodetype(client)
        client_another.ledger.terminateLedger(ledger_name, main_private_key)



    def test_cbft_sysconsensus_node_abnormal_notaffect_consensus(self, create_ledger_jion_three_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_jion_three_node
        client_another = clients[1]
        time.sleep(10)
        global_test_env.stop_designated_node(client_another.url)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        global_test_env.start_designated_node(client_another.url)
        for i in range(3):
            assert_blocknumber_growth(sys_ledger, ledger_name, client)


    def test_cbft_two_sysconsensus_node_abnormal_taffect_consensus(self, create_ledger_jion_three_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_jion_three_node
        client_another, client_another2 = clients[2], clients[3]
        time.sleep(10)
        global_test_env.stop_designated_node(client_another.url)
        global_test_env.stop_designated_node(client_another2.url)
        for i in range(5):
            assert_sys_blocknumber_notgrowth_sub_growth(sys_ledger, ledger_name, client)

        global_test_env.start_designated_node(client_another.url)
        assert_sys_blocknumber_notgrowth_sub_growth(sys_ledger, ledger_name, client)

        time.sleep(20)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        global_test_env.start_designated_node(client_another2.url)


    def test_cbft_two_sysconsensus_node_one_abnormal_taffect_consensus(self, clients, global_test_env):
        client = clients[0]
        node_list = client.node.listAll()
        data = json.loads(node_list[0])['data']
        node_name_list = [data[i]['name'] for i in range(len(data))]
        need_update_nodelist = [name for name in node_name_list if name[-4:] == '7789']
        for i in range(len(need_update_nodelist)-1):
            result = client.node.updateType(need_update_nodelist[i], 2, main_private_key)
            assert_code(result, 0)
        for i in range(len(clients)):
            if clients[i].url == 'http://192.168.16.121:7789':
                sys_consensus_client = clients[i]
            elif clients[i].url == 'http://192.168.16.121:7790':
                client_another = clients[i]
        time.sleep(5)
        ledger_name, sub_ledger_node = create_oneledger(client_another)
        time.sleep(5)
        join_result = client.ledger.joinLedger(ledger_name, sys_consensus_client.node_id, sys_consensus_client.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(3)
        add_result = sub_ledger_node.add(sys_consensus_client.node_id, sys_consensus_client.node_pubkey, main_private_key)
        assert_code(add_result, 0)

        time.sleep(10)
        global_test_env.stop_designated_node(sys_consensus_client.url)
        for i in range(5):
            assert_blocknumber_growth(sys_ledger, ledger_name, client_another)
        global_test_env.start_designated_node(client.url)
        time.sleep(30)
        assert_blocknumber_growth(sys_ledger, ledger_name, client_another)

        sys_updatenodetype(client)
        client_another.ledger.terminateLedger(ledger_name, main_private_key)



    def test_cbft_subconsensus_node_notabnormal_notaffect_consensus(self, create_ledger_four_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another = clients[4]
        time.sleep(10)
        global_test_env.stop_designated_node(client_another.url)
        time.sleep(3)
        for i in range(5):
            assert_blocknumber_growth(sys_ledger, ledger_name, client)
        global_test_env.start_designated_node(client_another.url)

        for i in range(5):
            assert_blocknumber_growth(sys_ledger, ledger_name, client)



    def test_cbft_two_subconsensus_node_abnormal_taffect_consensus(self, create_ledger_four_node, clients, global_test_env):
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another, client_another2 = clients[4], clients[5]
        time.sleep(10)
        global_test_env.stop_designated_node(client_another.url)
        global_test_env.stop_designated_node(client_another2.url)
        for i in range(5):
            assert_sys_blocknumber_growth_sub_notgrowth(sys_ledger, ledger_name, client)
        global_test_env.start_designated_node(client_another.url)
        assert_sys_blocknumber_growth_sub_notgrowth(sys_ledger, ledger_name, client)
        time.sleep(30)
        assert_blocknumber_growth(sys_ledger, ledger_name, client)

        global_test_env.start_designated_node(client_another2.url)




class TestLedgerConsensus():

    def test_samenode_separate_consensus(self, create_two_ledger):
        ledger_name_list, sub_ledger_node_list, client = create_two_ledger
        time.sleep(5)
        for i in range(3):
            assert_blocknumber_growth(ledger_name_list[0], ledger_name_list[1], client)


    def test_partlysamenode_separate_consensus(self, create_ledger_two_node, clients):
        ledger_name, _, client = create_ledger_two_node
        client_another = clients[5]
        another_ledger, sub_ledger_node, client= create_twonodes_ledger(client, client_another)
        time.sleep(5)
        for i in range(3):
            assert_blocknumber_growth(ledger_name, another_ledger, client)

        client.ledger.terminateLedger(another_ledger, main_private_key)


    def test_differentnode_separate_consensus(self, create_ledger_two_node, clients):
        ledger_name, _, client = create_ledger_two_node
        client_another = clients[2]
        another_ledger, _ = create_oneledger(client_another)
        time.sleep(5)
        for i in range(3):
            blocknumber_ledger1 = client.platone.blockNumber(ledger_name)
            blocknumber_ledger2 = client_another.platone.blockNumber(another_ledger)
            time.sleep(3)
            blocknumber_ledger1_after = client.platone.blockNumber(ledger_name)
            blocknumber_ledger2_after = client_another.platone.blockNumber(another_ledger)
            sub1_blockhigh_growth = blocknumber_ledger1_after - blocknumber_ledger1
            sub2_blockhigh_growth = blocknumber_ledger2_after - blocknumber_ledger2
            assert abs(sub1_blockhigh_growth - sub2_blockhigh_growth) <= 2
            assert blocknumber_ledger1_after > 0 and blocknumber_ledger2_after > 0

        client_another.ledger.terminateLedger(another_ledger, main_private_key)


    def test_sys_observenode_create_ledger_consecsusnode(self, clients):
        client, client_another = clients[0], clients[4]
        ledger_name, _ = create_oneledger(client_another)
        time.sleep(3)
        for i in range(5):
            blocknumber= client_another.platone.blockNumber(ledger_name)
            time.sleep(3)
            blocknumber_after = client_another.platone.blockNumber(ledger_name)
            assert 1 < blocknumber_after - blocknumber < 6

        client_another.ledger.terminateLedger(ledger_name, main_private_key)
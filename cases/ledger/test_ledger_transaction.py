from cases.ledger.conftest import *


class TestSysTransaction():

    def test_transaction(self, client):
        balance_befor = client.platone.getBalance(main_address)
        receive_balance_befor = client.platone.getBalance(user_address)
        transaction_receipt = transfer(main_private_key, user_address, 1, sys_ledger, client)
        assert transaction_receipt['status'] == 1
        balance_after = client.platone.getBalance(main_address)
        receive_balance_after = client.platone.getBalance(user_address)
        assert balance_befor - balance_after == receive_balance_after - receive_balance_befor == 1


    def test_sub_transaction(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        balance_befor = client.platone.getBalance(main_address, ledger=ledger_name)
        receive_balance_befor = client.platone.getBalance(user_address, ledger=ledger_name)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        assert transaction_receipt['status'] == 1
        balance_after = client.platone.getBalance(main_address, ledger=ledger_name)
        receive_balance_after = client.platone.getBalance(user_address, ledger=ledger_name)
        assert balance_befor - balance_after == receive_balance_after - receive_balance_befor == 1


    def test_numerous_transaction_noaffect(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        balance_befor_sys = client.platone.getBalance(main_address, ledger=sys_ledger)
        receive_balance_befor_sys = client.platone.getBalance(user_address, ledger=sys_ledger)
        balance_befor = client.platone.getBalance(main_address, ledger=ledger_name)
        receive_balance_befor = client.platone.getBalance(user_address, ledger=ledger_name)
        for i in range(5):
            for i in range(20):
                transaction_receipt = transfer(main_private_key, user_address, 1, sys_ledger, client)
                assert transaction_receipt['status'] == 1
            transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
            assert transaction_receipt['status'] == 1
        balance_after_sys = client.platone.getBalance(main_address, ledger=sys_ledger)
        receive_after_sys = client.platone.getBalance(user_address, ledger=sys_ledger)
        balance_after = client.platone.getBalance(main_address, ledger=ledger_name)
        receive_balance_after = client.platone.getBalance(user_address, ledger=ledger_name)
        assert balance_befor - balance_after == receive_balance_after - receive_balance_befor == 5
        assert balance_befor_sys - balance_after_sys == receive_after_sys - receive_balance_befor_sys == 100


    def test_check_transaction(self, transfer_info):
        client = transfer_info
        check_transaction_recepit = client.platone.getTransactionReceipt(client.transaction_hash, ledger = sys_ledger)
        assert client.transaction_receipt == check_transaction_recepit


    def test_sub_check_sys_transaction(self, create_ledger):
        ledger_name, _, client = create_ledger
        transaction_receipt = transfer(main_private_key, user_address, 1, sys_ledger, client)
        check_transaction_recepit = client.platone.getTransactionReceipt(transaction_receipt['transactionHash'], ledger = ledger_name)
        assert check_transaction_recepit is None

    def test_nonexistent_check_sys_transaction(self, client):
        transaction_receipt = transfer(main_private_key, user_address, 1, sys_ledger, client)
        check_transaction_recepit = client.platone.getTransactionReceipt(transaction_receipt['transactionHash'], ledger = 'xxxxx')
        assert check_transaction_recepit is None


    def test_sys_check_sub_transaction(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        check_transaction_recepit = client.platone.getTransactionReceipt(transaction_receipt['transactionHash'], ledger = sys_ledger)
        assert check_transaction_recepit is None


    def test_sub_check_sub_transaction(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        time.sleep(3)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        check_transaction_recepit = client.platone.getTransactionReceipt(transaction_receipt['transactionHash'], ledger = ledger_name)
        assert check_transaction_recepit == check_transaction_recepit


    def test_another_check_sub_transaction(self, create_two_ledger):
        ledger_name_list, _, client = create_two_ledger
        time.sleep(3)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name_list[0], client)
        check_transaction_recepit = client.platone.getTransactionReceipt(transaction_receipt['transactionHash'], ledger = ledger_name_list[1])
        assert check_transaction_recepit is None

    def test_nonexistent_check_transaction(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        check_transaction_recepit = client.platone.getTransactionReceipt(transaction_receipt['transactionHash'], ledger='xxxxx')
        assert check_transaction_recepit is None




class TestNonce():


    def test_noaffect_nonce(self, create_two_ledger):
        ledger_name_list, _, client = create_two_ledger
        time.sleep(3)
        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name_list[0], client)
        assert transaction_receipt['status'] == 1
        sys_nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        sub1_nonce = client.platone.getTransactionCount(main_address, ledger=ledger_name_list[0])
        sub2_nonce = client.platone.getTransactionCount(main_address, ledger=ledger_name_list[1])
        assert sys_nonce != sub1_nonce
        assert sub1_nonce - sub2_nonce == 1


    def test_block_noaffect_nonce(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        status = client.txpool.status(ledger_name)
        assert status['queued'] == '0x0'
        try:
            nonce = client.platone.getTransactionCount(main_address, ledger=ledger_name)
            transaction_dict = {
                "to": user_address,
                "gasPrice": client.platone.gasPrice(ledger_name),
                "gas": 21000,
                "nonce": nonce + 1,
                "data": '',
                "chainId": client.chain_id,
                "value": 1,
            }
            signedTransactionDict = client.platone.account.signTransaction(
                transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
            )
            data = signedTransactionDict.rawTransaction
            tx_hash = HexBytes(client.platone.sendRawTransaction(data, ledger_name)).hex()
            transaction_receipt = client.platone.waitForTransactionReceipt(tx_hash, ledger_name)
        except:
            status = client.txpool.status(ledger_name)
        assert status['queued'] == '0x1'
        transaction_receipt = transfer(main_private_key, user_address, 1, sys_ledger, client)
        assert transaction_receipt['status'] == 1
        status = client.txpool.status(ledger_name)
        assert status['queued'] == '0x1'


    def test_block_noaffect_sub_nonce(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        status = client.txpool.status(sys_ledger)
        assert status['queued'] == '0x0'
        try:
            nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
            transaction_dict = {
                "to": user_address,
                "gasPrice": client.platone.gasPrice(sys_ledger),
                "gas": 21000,
                "nonce": nonce + 1,
                "data": '',
                "chainId": client.chain_id,
                "value": 1,
            }
            signedTransactionDict = client.platone.account.signTransaction(
                transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
            )
            data = signedTransactionDict.rawTransaction
            tx_hash = HexBytes(client.platone.sendRawTransaction(data, sys_ledger)).hex()
            transaction_receipt = client.platone.waitForTransactionReceipt(tx_hash, sys_ledger)
        except:
            status = client.txpool.status(sys_ledger)
        assert status['queued'] == '0x1'

        transaction_receipt = transfer(main_private_key, user_address, 1, ledger_name, client)
        assert transaction_receipt['status'] == 1
        status = client.txpool.status(sys_ledger)
        assert status['queued'] == '0x1'



    def test_discard_noaffect_nonce(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        status = client.txpool.status(ledger_name)
        assert status['queued'] == '0x0'
        try:
            nonce = client.platone.getTransactionCount(main_address, ledger=ledger_name)
            transaction_dict = {
                "to": user_address,
                "gasPrice": client.platone.gasPrice(ledger_name),
                "gas": 21000,
                "nonce": nonce + 1,
                "data": '',
                "chainId": client.chain_id,
                "value": 1,
            }
            signedTransactionDict = client.platone.account.signTransaction(
                transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
            )
            data = signedTransactionDict.rawTransaction
            tx_hash = HexBytes(client.platone.sendRawTransaction(data, ledger_name)).hex()
            transaction_receipt = client.platone.waitForTransactionReceipt(tx_hash, ledger_name)
        except:
            status = client.txpool.status(ledger_name)
        assert status['queued'] == '0x1'
        #todo: 等3小时之后验证系统账本发起交易，且不会影响丢失的子帐本交易


    def test_discard_noaffect_sub_nonce(self, create_ledger):
        ledger_name, _, client = create_ledger
        time.sleep(3)
        status = client.txpool.status(sys_ledger)
        assert status['queued'] == '0x0'
        try:
            nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
            transaction_dict = {
                "to": user_address,
                "gasPrice": client.platone.gasPrice(sys_ledger),
                "gas": 21000,
                "nonce": nonce + 1,
                "data": '',
                "chainId": client.chain_id,
                "value": 1,
            }
            signedTransactionDict = client.platone.account.signTransaction(
                transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
            )
            data = signedTransactionDict.rawTransaction
            tx_hash = HexBytes(client.platone.sendRawTransaction(data, sys_ledger)).hex()
            transaction_receipt = client.platone.waitForTransactionReceipt(tx_hash, sys_ledger)
        except:
            print('except')
            status = client.txpool.status(sys_ledger)
        assert status['queued'] == '0x1'
        # todo: 等3小时之后验证子账本发起交易，且不会影响丢失的系统帐本交易


    def test_replace_noaffect_nonce(self, create_ledger):
        #todo: 替换调不通
        ledger_name, _, client = create_ledger
        platone = client.platone
        time.sleep(3)
        status = client.txpool.status(sys_ledger)
        assert status['queued'] == '0x0'
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce + 1,
            "data": '',
            "chainId": client.chain_id,
            "value": 1,
        }
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        # aaa = HexBytes(platone.sendRawTransaction(data, sys_ledger))
        bbb = platone.sendRawTransaction(data, sys_ledger)
        # tx_hash = HexBytes(platone.sendRawTransaction(data, sys_ledger)).hex()
        try:
            # nonce = platone.getTransactionCount(main_address, ledger=ledger_name)
            # transaction_dict = {
            #     "to": user_address,
            #     "gasPrice": platone.gasPrice(ledger_name),
            #     "gas": 21000,
            #     "nonce": nonce + 1,
            #     "data": '',
            #     "chainId": chain_id,
            #     "value": 1,
            # }
            # signedTransactionDict = platone.account.signTransaction(
            #     transaction_dict, main_private_key, net_type=w3.net_type, mode='SM'
            # )
            # data = signedTransactionDict.rawTransaction
            # tx_hash = HexBytes(platone.sendRawTransaction(data, ledger_name)).hex()
            transaction_receipt = platone.waitForTransactionReceipt(HexBytes(bbb).hex(), sys_ledger)
            print(transaction_receipt)
        except:
            status = client.txpool.status(sys_ledger)
            print(status)
        # result = personal.importRawKey(main_private_key, '12345678')
        # assert result == main_address
        time.sleep(5)
        result = client.personal.unlockAccount(main_address, '12345678')
        print(f'替换结果={result}')
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger) + 100,
            "gas": 21000 + 100,
            "nonce": nonce + 1,
            "data": '',
            "chainId": client.chain_id,
            "value": 1,
        }
        result = platone.replaceTransaction(bbb, transaction_dict, sys_ledger)
        print(result)



    def test_nonexistent_ledger_transaction(self, client):
        ledger_name = 'nonexistent_ledger'
        status = False
        try:
            result = transfer(main_private_key, user_address, 1, ledger_name, client)
        except:
            status = True
        assert status
        result = transfer(main_private_key, user_address, 1, sys_ledger, client)
        assert result['status'] == 1






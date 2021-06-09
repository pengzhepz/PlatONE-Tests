from cases.ledger.conftest import *

class TestGas():



    def test_nobalance_transaction(self, client):
        balance = client.platone.getBalance(visitor_address)
        if balance != 0:
            result = transfer(visitor_private_key, user_address, balance, sys_ledger, client)
            assert result['status'] == 1
        result = transfer(visitor_private_key, user_address, 0, sys_ledger, client)
        assert result['status'] == 1


    def test_subledger_nobalance_transaction(self, create_ledger):
        ledger_name, sub_ledger_node, client = create_ledger
        time.sleep(3)
        balance = client.platone.getBalance(visitor_address, ledger=ledger_name)
        if balance != 0:
            result = transfer(visitor_private_key, user_address, balance, ledger_name, client)
            assert result['status'] == 1
        result = transfer(visitor_private_key, user_address, 0, ledger_name, client)
        assert result['status'] == 1


    def test_same_estimate_for_different_ledgers(self, create_ledger_three_node):
        ledger_name, _, client = create_ledger_three_node
        time.sleep(3)
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": hex(client.platone.gasPrice(sys_ledger)),
            "gas": hex(21000),
            "nonce": hex(nonce),
            "data": '',
            "chainId": client.chain_id,
            "value": hex(0),
        }
        estimateGas = client.platone.estimateGas(transaction_dict, ledger=sys_ledger)
        estimateGas_subledger = client.platone.estimateGas(transaction_dict, ledger=ledger_name)
        assert estimateGas == estimateGas_subledger


    def test_transaction_doesnot_consume_gas(self, create_ledger_three_node):
        ledger_name, _, client = create_ledger_three_node
        sys_balance = client.platone.getBalance(main_address, ledger=sys_ledger)
        sys_tranasction = transfer(main_private_key, user_address, 1, sys_ledger, client)
        assert sys_tranasction['status'] == 1
        sys_balance_after = client.platone.getBalance(main_address, ledger=sys_ledger)
        assert sys_balance - sys_balance_after == 1

        sub_balance = client.platone.getBalance(main_address, ledger=ledger_name)
        sub_tranasction = transfer(main_private_key, user_address, 1, ledger_name, client)
        assert sub_tranasction['status'] == 1
        sub_balance_after = client.platone.getBalance(main_address, ledger=ledger_name)
        assert sub_balance - sub_balance_after == 1


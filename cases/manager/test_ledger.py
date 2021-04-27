import pytest
from lib.mgrui.locator.ledgerPage import LedgerPage


@pytest.fixture(scope='class')
def ledger_page(login):
    return LedgerPage(login)


class TestLedger:

    def test_add_ledger_success(self, ledger_page):
        """
        添加账本
        """
        ledger_page.add_ledger(name='tLedger')
        assert ledger_page.check_toast('新建账本成功!') is True

    def test_close_ledger_success(self, ledger_page):
        """
        关闭账本
        """
        ledger_page.close_ledger()
        assert ledger_page.check_toast('账本关闭成功!') is True

    def test_add_ledger_fail(self, ledger_page):
        """
        仅选择观察者节点,创建账本
        """
        ledger_page.add_ledger('dledger', index=1)
        assert ledger_page.check_add_node_fail('请至少添加一个共识节点') is True

    def test_altogether_ledger(self, ledger_page):
        """
        添加所有现存的节点的账本
        """
        ledger_page.add_all('aledger')
        assert ledger_page.check_toast('新建账本成功!') is True

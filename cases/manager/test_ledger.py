import pytest
from lib.mgrui.locator.ledgerPage import LedgerPage
import random
import string


@pytest.fixture(scope='class')
def ledger_page(login):
    return LedgerPage(login)


class TestLedger:

    def setup_method(self):
        # 随机账本名
        self.name = ''.join(random.sample(string.ascii_letters, 3))

    def test_add_ledger_success(self, ledger_page):
        """
        添加账本,仅选择一个共识节点
        """
        ledger_page.add_ledger(self.name)
        assert ledger_page.check_text('新建账本成功!') is True

    def test_close_ledger_success(self, ledger_page):
        """
        删除账本
        """
        ledger_page.close_ledger()
        assert ledger_page.check_text('账本关闭成功!') is True

    def test_add_ledger_fail(self, ledger_page):
        """
        创建账本，仅选择观察者节点
        """
        ledger_page.add_ledger(self.name, index=1)
        assert ledger_page.check_text('请至少添加一个共识节点') is True

    def test_altogether_ledger(self, ledger_page):
        """
        添加所有现存的节点的账本
        """
        ledger_page.add_specify_node(self.name)
        assert ledger_page.check_text('新建账本成功!') is True

    def test_enter_ledger_detail(self, ledger_page):
        """
        进入账本详情
        """
        ledger_page.enter_ledger_detail()
        assert ledger_page.check_text('账本详情') is True

    def test_nond_ledger(self, ledger_page):
        """
        不添加任何节点，然后创建账本
        预期结果：添加失败
        """
        ledger_page.add_specify_node(self.name, auto=False)
        assert ledger_page.check_text('请至少添加一个共识节点') is True

    def test_no_publicnd_ledger(self, ledger_page):
        """
        添加账本，添加所有节点除了共识节点
        预期结果：添加失败
        """
        ledger_page.add_specify_node(self.name, start=1)
        assert ledger_page.check_text('请至少添加一个共识节点') is True

    def test_repeat_add_ledger(self, ledger_page):
        """
        添加重名的账本
        预期结果：添加失败
        """
        x = self.name
        ledger_page.add_ledger(name=x)
        import time
        time.sleep(4)
        ledger_page.add_ledger(name=x)
        assert ledger_page.check_text('账本名称已存在') is True

    def test_no_auth_add_ledger(self, specify_login):
        """
        无权限者添加账本
        预期结果：没有账本管理入口，无法添加
        """
        spec_ledger_page = LedgerPage(specify_login)  # 指定账号登录
        try:
            spec_ledger_page.select_ledger_index()
        except BaseException as b:
            print(b)
            assert spec_ledger_page.check_text('账本管理') is False

    def test_add_node2Ledger(self, ledger_page):
        """
        为已存在的账本，添加节点（此节点也已经同步完主节点的区块）
        预期结果：可直接添加成功
        """
        ledger_page.enter_ledger_detail(index=1)  # 进入第一个账本
        ledger_page.add_ledger_node(num=1)  # 加一个
        assert ledger_page.check_text('添加节点成功!') is True

    def test_modify_to_publicnd(self, ledger_page):
        """
        修改账本中的观察者节点为共识节点
        """
        ledger_page.enter_ledger_detail(index=1)
        ledger_page.modify_2pulicnode(num=1)
        assert ledger_page.check_text('修改成功') is True

    def test_modify_tonormalnd(self, ledger_page):
        """
        修改账本中的共识节点为观察者节点
        """
        ledger_page.enter_ledger_detail(index=1)
        ledger_page.modify_2noramlnode(num=1)
        assert ledger_page.check_text('修改成功') is True

    def test_delete_normalnd(self, ledger_page):
        """
        1.进入账本详情
        2.删除其中一个观察者节点
        """
        ledger_page.enter_ledger_detail(index=2)
        ledger_page.delete_node(num=1)
        assert ledger_page.check_text('删除成功') is True

    def test_recycle_author(self, ledger_page):
        """
        回收权限
        """
        ledger_page.enter_ledger_detail()
        ledger_page.re_authorize(index=2)
        assert ledger_page.check_text('回收权限成功') is True

    def test_authorize_success(self, ledger_page):
        """
        授权用户
        """
        ledger_page.enter_ledger_detail()
        ledger_page.authorize(inidex=2)  # 对第二个用户授权
        assert ledger_page.check_text('授权成功') is True

    def test_no_author(self, ledger_page):
        """
        ：TODO： 没有权限操作账本
        """
        pass

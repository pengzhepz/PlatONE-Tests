import time

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

    def test_01_add_ledger_success(self, ledger_page):
        """
        添加账本,仅选择一个共识节点
        """
        ledger_page.add_ledger(self.name)
        assert ledger_page.check_text('新建账本成功!') is True

    def test_02_close_ledger(self, ledger_page):
        """
        删除账本
        """
        ledger_page.close_ledger()
        assert ledger_page.check_text('账本关闭成功!') is True

    def test_03_add_ledger_fail(self, ledger_page):
        """
        创建账本，仅选择观察者节点
        """
        try:
            ledger_page.add_ledger(self.name, index=1)
            assert ledger_page.check_text('请至少添加一个共识节点') is True
        finally:
            ledger_page.close_ledger_window()

    def test_04_altogether_ledger(self, ledger_page):
        """
        添加所有现存的节点的账本
        """
        ledger_page.add_specify_node(self.name)
        assert ledger_page.check_text('新建账本成功!') is True

    def test_05_enter_ledger_detail(self, ledger_page):
        """
        进入账本详情
        """
        ledger_page.enter_ledger_detail()
        assert ledger_page.check_text('新增节点') is True

    def test_06_nond_ledger(self, ledger_page):
        """
        不添加任何节点，然后创建账本
        预期结果：添加失败
        """
        try:
            ledger_page.add_specify_node(self.name, auto=False)
            assert ledger_page.check_text('请至少添加一个共识节点') is True
        finally:
            ledger_page.close_ledger_window()

    def test_07_no_publicnd_ledger(self, ledger_page):
        """
        添加账本，添加所有节点除了共识节点
        预期结果：添加失败
        """
        try:
            ledger_page.add_specify_node(self.name, start=1)
            assert ledger_page.check_text('请至少添加一个共识节点') is True
        finally:
            ledger_page.close_ledger_window()

    def test_08_repeat_add_ledger(self, ledger_page):
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

    @pytest.mark.skip('有问题')
    def test_09_no_auth_add_ledger(self, specify_login):
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

    def test_10_add_node2Ledger(self, ledger_page):
        """
        为已存在的账本，添加节点（此节点也已经同步完主节点的区块）
        预期结果：可直接添加成功
        """
        try:
            ledger_page.enter_ledger_detail(index=1)  # 进入第一个账本
            ledger_page.add_ledger_node(num=1)  # 加一个
            assert ledger_page.check_text('添加节点成功!') is True
        finally:
            ledger_page.select_ledger_index()

    @pytest.mark.skip('测试数据原因，暂时跳过')
    def test_11_modify_to_publicnd(self, ledger_page):
        """
        修改账本中的观察者节点为共识节点
        """
        ledger_page.enter_ledger_detail(index=1)
        ledger_page.modify_2pulicnode(num=1)
        assert ledger_page.check_text('修改成功') is True

    @pytest.mark.skip('测试数据原因，暂时跳过')
    def test_12_modify_tonormalnd(self, ledger_page):
        """
        修改账本中的共识节点为观察者节点
        """
        ledger_page.enter_ledger_detail(index=1)
        ledger_page.modify_2noramlnode(num=1)
        assert ledger_page.check_text('修改成功') is True

    def test_13_delete_normalnd(self, ledger_page):
        """
        1.进入账本详情
        2.删除其中一个观察者节点
        """
        ledger_page.enter_ledger_detail(index=2)
        ledger_page.delete_node(num=1)
        assert ledger_page.check_text('删除成功') is True

    def test_14_recycle_author(self, ledger_page):
        """
        回收权限
        """
        try:
            ledger_page.enter_ledger_detail()
            ledger_page.re_authorize(index=1)
            assert ledger_page.check_text('回收权限成功') is True
        finally:
            ledger_page.close_ledger_window()

    def test_15_authorize_success(self, ledger_page):
        """
        授权用户
        """
        try:
            ledger_page.enter_ledger_detail()
            ledger_page.authorize(index=1)
            assert ledger_page.check_text('授权成功') is True
        finally:
            ledger_page.close_ledger_window()

    @pytest.mark.skip('有问题')
    def test_16_no_author(self, no_author_login):
        """
        ：TODO： 跟test_recycle_author方法紧密关联，得解耦
        """
        spec_ledger_login = LedgerPage(no_author_login)
        spec_ledger_login.enter_ledger_detail(index=1)
        spec_ledger_login.add_ledger_node(num=1)
        assert spec_ledger_login.check_text('权限拒绝') is True

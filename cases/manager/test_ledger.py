import time
import pytest
from lib.mgrui.urls import ledger_url
from lib.mgrui.locator.ledgerPage import LedgerPage
from lib.mgrui.locator.loginPage import LoginPage
from lib.mgrui.data.get_ui_data import get_data


@pytest.fixture(scope='class')
def bill_page(driver):
    driver.get(ledger_url)
    lp = LoginPage(driver)
    lp.set_chain('192.168.120.133', '1331')
    time.sleep(1)
    file = r'C:\Users\juzix\Desktop\lax19my0865mde2dlmujpa6l2z397mlwwrsn8lthur.json'
    lp.login(file, '12345678')
    lp.index(3)
    return LedgerPage(driver)


class TestLedger:
    cases, parameters = get_data(r'../../lib/mgrui/data/bill.yaml')

    @pytest.mark.parametrize("params,expected", parameters, ids=cases)
    def test_add_ledger_success(self, bill_page, params, expected):
        """
        TODO: 断言
        """
        bill_page.add_bill(params['name'], params['id'])

    def test_close_ledger_success(self, bill_page, index=1):
        """
        TODO: 断言
        """
        bill_page.close_bill(index)

import pytest
from lib.mgrui.locator.ledgerPage import LedgerPage
from common.getYaml import get_data


@pytest.fixture(scope='class')
def bill_page(driver):
    return LedgerPage(driver)


class TestLedger:
    cases, parameters = get_data(r'../../data/ui/ledger.yaml')

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

import time
import pytest
from lib.mgrui.urls import ledger_url
from lib.mgrui.locator.nodePage import NodePage
from lib.mgrui.locator.loginPage import LoginPage
from lib.mgrui.data.get_ui_data import get_data


@pytest.fixture(scope='class')
def node_page(driver):
    driver.get(ledger_url)
    lp = LoginPage(driver)
    lp.set_chain('192.168.120.133', '1331')
    time.sleep(1)
    file = r'C:\Users\juzix\Desktop\lax19my0865mde2dlmujpa6l2z397mlwwrsn8lthur.json'
    lp.login(file, '12345678')
    lp.index(2)
    return NodePage(driver)



class TestNode:
    cases, parameters = get_data(r'../../lib/mgrui/data/node.yaml')

    @pytest.mark.parametrize("params,expected", parameters, ids=cases)
    def test_add_node_success(self, node_page, params, expected):
        """
        TODO: 断言结果
        """
        node_page.add_node(params['name'], params['desc'], params['rpc'], params['license_file'], params['ip'],
                           params['pwd'], params['host'], params['p2pport'], params['genesis_file'], params['script'],
                           params['user'], params['dock'])

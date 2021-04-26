import pytest
from lib.mgrui.locator.nodePage import NodePage
from common.getYaml import get_data


@pytest.fixture(scope='class')
def node_page(login):
    return NodePage(login)


class TestNode:
    cases, parameters = get_data(r'../../data/ui/node.yaml')

    @pytest.mark.parametrize("params,expected", parameters, ids=cases)
    def test_add_node_success(self, node_page, params, expected):
        """
        TODO: 断言结果
        """
        node_page.add_node(params['name'], params['desc'], params['rpc'], params['license_file'], params['ip'],
                           params['pwd'], params['host'], params['p2pport'], params['genesis_file'], params['script'],
                           params['user'], params['dock'])

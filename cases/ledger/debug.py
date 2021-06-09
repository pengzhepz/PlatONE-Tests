
from cases.ledger.conftest import *
from common.getYaml import LoadFile



# main_address, main_private_key = 'lax17sfqr79fzq6qgx3x9wv8259mjjjstjfhjyue4p', 'dfe074dc29a259f23c4dbca369faee16a82528af2324ef230811db89a704e8b6'
# user_address, user_private_key = 'lax1yyc4fcrqmfw9g3urw7t7jj4qwp4cfmwpl5g705', '802158ca03ed58d0115d4d84e325c312521629be3afbbe08a12de641b5f59b92'
# chain_admin_address, chain_admin_private_key = 'lax1u2rlvu2x545r84yjw6hcgewe9axmmgp9tc4yne', 'adb0fa48bbba6f4e64e1b9517d3a67378399d48d5c6a2509972bb7758ad1f8fa'
# node_admin_address, node_admin_private_key = 'lax1lwhhmxm9pxqj6k9ev35psvzf4lxyx625pgeh0z', '3d3a16b247bc8064833e2e6a131cdb61e9587dd9c8c6564196c0e459a6ffa526'
# contract_admin_address, contract_admin_private_key = 'lax1m7qam7mxk3zwtj4vkwr2zfstuzmy4u3xaxhlxn', 'f9329cb010460afb375f19093ac886e4a10a7d9dbe02e903d91e519b94199207'
# contract_deployer_address, contract_deployer_private_key ='lax139kdt6lc5f2npcmvxvwg89q9khf8zdg3cyxq6s', '3152b678c37ab821644ac82812d0f00b281cb58e5d658b695ef8c5610a4da726'
# visitor_address, visitor_private_key = 'lax1hg4pa8vpqzd8c2ncz39kvvpq7hgn9pc7pmusjd', '242db3a9a14d5345e23caee4ac0e705f1489efa487e4cfddcf44ef9d64895f11'


# def test_001(clients):
#     client = clients[0]
#     # # client1 = clients[2]
#     print(f'debug  listall={client.node.listAll()}')
    # name = 'ROOT-NODE-1'
    # host_address = '192.168.16.121'
    # rpc_port =7789
    # p2p_port = 17789
    # desc = ''
    # private_key = main_private_key
    # result = client.node.update(name, host_address, rpc_port, p2p_port, desc, private_key)
    # print(result)
    # time.sleep(5)
    # print(f'debug wait  listall={client.node.listAll()}')
    # print(type(client.host), client.host)
    # print(type(client.rpc_port), client.rpc_port)
    # print(type(client.p2p_port), client.p2p_port)
    # print(type(main_private_key), main_private_key)
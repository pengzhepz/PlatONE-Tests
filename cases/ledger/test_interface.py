
import pytest
from hexbytes import HexBytes
from platone import Web3, HTTPProvider, platone, txpool, Account, miner, net, personal
from cases.ledger.conftest import *


class TestInterface:

    def test_protocolVersion(self):
        """
        @describe: 获取当前以太坊协议的版本
        @parameters:
        - 1. null
        @return:
        - 1. 当前以太坊协议的版本,String
        """
        version = platone.protocolVersion
        assert version == '63'


    def test_syncing(self):
        """
        不知道怎么断言，先留着吧
        @describe: 检查节点当前是否已经与网络同步
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. Object或Bool。如果节点尚未与网络同步，则返回false，否则返回一个同步对象
        """
        result = platone.syncing(ledger)
        print(result)


    def test_gasPrice(self):
        """
        @describe: 获取当前gas价格，该价格由最近的若干块的gas价格中值决定。
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. 当前gas价格,int
        """
        gasPrice = platone.gasPrice(ledger)
        assert gasPrice == 1000000000


    def test_accounts(self):
        """
        不知道怎么断言，先留着吧
        @describe: 获取当前节点控制的账户列表
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. 返回当前节点控制的账户列表,list
        """
        accounts = platone.accounts(ledger)
        print(accounts)


    def test_blockNumber(self):
        """
        @describe: 获取当前块编号
        @parameters:
        - 1. ledger: 账本名称
        @return:
        - 1. 返回当前块编号,int
        """
        blocknumber = platone.blockNumber(ledger)
        print(blocknumber)
        assert isinstance(blocknumber, int) and blocknumber >= 0


    def test_evidences(self):
        """
        @describe: 获取账户地址指定位置的存储内容
        @parameters:
        - 1. account： ledger： 账本名称
        @return:
        - 1. 账户地址指定位置的存储内容,AttributeDict
        """
        evidences = platone.evidences(ledger)
        assert isinstance(evidences, dict)

    def test_consensusStatus(self):
        """
        @describe: 获取当前节点所在区块树的共识状态信息
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. 当前节点所在区块树的共识状态信息,AttributeDict
        """
        status_info = platone.consensusStatus(ledger)
        # print(status_info)
        # print(platone.blockNumber(ledger))
        blochnumber = status_info['blockTree']['root']['blockNumber']
        assert 0 <= platone.blockNumber(ledger) - blochnumber <= 3


    def test_getPrepareQC(self, transfer_info):
        """
        预期结果是什么暂时没有查到，先留着吧
        @describe: 获取
        @parameters:
        - 1. block_number： 块高
        - 2. ledger： 账本名称
        @return:
        - 1. 指定块中特定账户地址的余额,AttributeDict
        """
        prepare = platone.getPrepareQC(transfer_info.block_identifier, ledger)
        print(prepare)
        prepare_blocknumber = prepare['blockNumber']
        assert prepare_blocknumber == transfer_info.block_identifier


    def test_getbalance(self):
        """
        @describe: 获取指定块中特定账户地址的余额
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块中特定账户地址的余额,int
        """
        balance = platone.getBalance(user_address, ledger=ledger)
        assert isinstance(balance, int) and balance >= 0


    def test_getStorageAt(self, transfer_info):
        """
        返回值不是应该是一个储存内容，不太懂先留着吧
        @describe: 获取一个地址的指定位置存储内容
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. position： 存储中的索引编号, Number
        - 3. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 4. ledger:  账本名称
        @return:
        - 1. 一个地址的指定位置存储内容
        """
        storage = platone.getStorageAt(main_address, 1, transfer_info.block_identifier, ledger=ledger)
        print(type(storage))
        print(storage)


    def test_getCode(self):
        """
        返回值是不太对，应该传什么地址才能有结果呢，先留着吧
        @describe: 获取指定地址处的代码
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 指定地址处的代码
        """
        balance = platone.getCode(main_address, ledger=ledger)
        print(balance)
        print(type(balance))


    def test_getBlock(self):
        """
        不会，留着吧
        @describe: 获取指定块编号或块哈希对应的块
        @parameters:
        - 1. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 2. full_transactions: Boolean -  可选，默认值为false。当设置为true时,返回块中将包括所有交易详情，否则仅返回交易哈希
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块编号或块哈希对应的块
        """
        block = platone.getBlock("latest", ledger=ledger)
        print(block)


    def test_getBlockTransactionCount(self, transfer_info):
        """
        @describe: 获取指定块中的交易数量
        @parameters:
        - 1. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 2. ledger： 账本名称
        @return:
        - 1. 返回指定块中的交易数量,int
        """
        count = platone.getBlockTransactionCount(transfer_info.block_identifier, sys_ledger)
        assert isinstance(count, int) and count >= 0


    def test_getTransaction(self, transfer_info):
        """
        @describe: 获取具有指定哈希值的交易对象
        @parameters:
        - 1. transaction_hash： 要查询的交易的哈希值
        - 2. ledger： 账本名称
        @return:
        - 1. 具有指定哈希值的交易对象,AttributeDict
        """
        result = platone.getTransaction(transfer_info.transaction_hash.hex(), ledger)
        assert result['hash'] == transfer_info.transaction_hash and result['blockNumber'] == transfer_info.block_identifier


    def test_getRawTransaction(self, transfer_info):
        """
        @describe: 获取具有指定哈希值的交易对象HexBytes 值
        @parameters:
        - 1. transaction_hash： 要查询的交易的哈希值
        - 2. ledger： 账本名称
        @return:
        - 1. 具有指定哈希值的交易对象HexBytes 值,
        """
        raw_transaction = platone.getRawTransaction(transfer_info.transaction_hash.hex(), ledger)
        #断言什么？先留着吧


    def test_getTransactionFromBlock(self, transfer_info):
        """
        @describe: 获取指定块中特定索引号的交易对象
        @parameters:
        - 1. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 2. transaction_index：交易索引位置 -Number
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块中特定索引号的交易对象，AttributeDict
        """
        block = platone.getTransactionFromBlock(transfer_info.block_identifier, transfer_info.transaction_index, ledger)
        assert transfer_info.transaction_hash == block['hash']


    def test_getTransactionByBlock(self, transfer_info):
        """
        @describe: 获取指定块中特定索引号的交易对象
        @parameters:
        - 1. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 2. transaction_index：交易索引位置 -Number
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块中特定索引号的交易对象,AttributeDict
        """
        block = platone.getTransactionByBlock(transfer_info.block_identifier, transfer_info.transaction_index, ledger)
        assert transfer_info.transaction_hash == block['hash']


    def test_waitForTransactionReceipt(self, transfer_info):
        """
        @describe: 获取指定时间内返回指定交易的收据对象
        @parameters:
        - 1. transaction_hash： 交易的哈希值 -String
        - 2. ledger： 账本名称
        - 3. timeout： 可选的等待时间长度，单位为秒。默认为120 -Number
        @return:
        - 1. 指定时间内返回指定交易的收据对象,AttributeDict
        """
        receipt = platone.waitForTransactionReceipt(transfer_info.transaction_hash.hex(), ledger, 120)
        assert receipt == transfer_info.transaction_receipt


    def test_getTransactionReceipt(self, transfer_info):
        """
        @describe: 指定交易的收据对象。如果交易处于pending状态，则返回null
        @parameters:
        - 1. transaction_hash： 交易的哈希值 -String
        - 2. ledger： 账本名称
        @return:
        - 1. 指定交易的收据对象。如果交易处于pending状态，则返回null
        """
        receipt = platone.getTransactionReceipt(transfer_info.transaction_hash.hex(), ledger)
        assert receipt == transfer_info.transaction_receipt
        transaction_hash1 = '123'
        receipt1 = platone.getTransactionReceipt(transaction_hash1, ledger)
        assert receipt1 is None


    def test_getTransactionCount(self, transfer_info):
        """
        @describe: 获取指定地址发出的交易数量
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块中特定账户地址的余额,int
        """
        count = platone.getTransactionCount(main_address, transfer_info.block_identifier, ledger)
        transaction = transfer(main_private_key, user_address, 1 * 10 ** 18, sys_ledger)
        block = transaction['blockNumber']
        count1 = platone.getTransactionCount(main_address, block, ledger)
        assert count1 - 1 == count

    def test_replaceTransaction(self):
        """
        todo:不会，pending池场景不会造，先留着吧
        @describe: 发送新的交易new_transaction，替代原来的交易transaction_hash（pending状态）
        @parameters:
        - 1. transaction_hash： 处于pending状态的交易的hash值
        - 2. new_transaction： 交易对象，包含字段与sendTransaction中的transactionObject一致。
        - 3. ledger： 账本名称
        @return:
        - 1. new_transaction 的hash值
        """
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce + 1,
            "data": '',
            "chainId": chain_id,
            "value": 1,
        }
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=w3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        tx_hash = HexBytes(platone.sendRawTransaction(data, sys_ledger)).hex()
        print(tx_hash)
        print(txpool.content(sys_ledger))

        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger) + 1,
            "gas": 21000 * 2,
            "nonce": nonce + 1,
            "data": '123',
            "chainId": chain_id,
            "value": 1 * 10 ** 18,
        }
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=w3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        balance = platone.replaceTransaction(tx_hash, data, sys_ledger)
        print(balance)
        print(txpool.content(sys_ledger))


    def test_modifyTransaction(self):
        """
        todo:不会造pending场景，先放着吧
        @describe: 发送新的参数，去修正处于pending状态的交易
        @parameters:
        - 1. transaction_hash： 处于pending状态的交易的hash值。
        - 2. ledger： 账本名称
        - 3. **transaction_params: 与transaction_hash的参数对应的关键词语句。如 value=1000,将原交易中的value值改为1000
        @return:
        - 1. 修正后的交易的hash值
        """
        balance = platone.modifyTransaction()

    def test_sendTransaction(self):
        """
        有问题需要星哥改sdk
        @describe: 向platone 链上提交一个交易
        @parameters:
        - 1. transaction： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. ledger： 账本名称
        @return:
        - 1. 32字节长的交易哈希值?
        """
        from_address = Account.privateKeyToAccount(main_private_key, hrp, mode='SM').address
        nonce = platone.getTransactionCount(from_address, ledger=ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": hex(platone.gasPrice(ledger)),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": chain_id,
            "value": 1 * 10 ** 18,
        }
        balance = platone.sendTransaction(transaction_dict, ledger)
        print(balance)


    def test_sendRawTransaction(self):
        """
        @describe: 向platone 链上提交一个签名的序列化的交易
        @parameters:
        - 1. raw_transaction： 要发送的签名交易对象.包含以下字段：
            - from - String|Number: 交易发送方账户地址，不设置该字段的话，则使用platone.defaultAccount属性值。可设置为一个地址或本地钱包platone.accounts.wallet中的索引序号
            - to - String: 可选，消息的目标地址，对于合约创建交易该字段为null
            - value - Number|String|BN|BigNumber: (optional) The value transferred for the transaction in VON, also the endowment if it’s a contract-creation transaction.
            - gas - Number: 可选，默认值：待定，用于交易的gas总量，未用完的gas会退还
            - gasPrice - Number|String|BN|BigNumber: 可选，该交易的gas价格，单位为VON，默认值为platone.gasPrice属性值
            - data - String: 可选，可以是包含合约方法数据的ABI字符串，或者是合约创建交易中的初始化代码
            - nonce - Number: 可选，使用该字段覆盖使用相同nonce值的挂起交易
            - main_private_key: 用于前面的私钥
        - 2. ledger： 账本名称
        @return:
        - 1. 包含32字节长的交易哈希值的HexBytes
        """
        from_address = Account.privateKeyToAccount(main_private_key, hrp, mode='SM').address
        nonce = platone.getTransactionCount(from_address, ledger=ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": chain_id,
            "value": 1 * 10 ** 18,
        }
        print(f'transaction_dict: {transaction_dict}')
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=w3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        tx_hash = platone.sendRawTransaction(data, ledger)
        assert isinstance(tx_hash, HexBytes)


    def test_sign(self):
        """
        @describe: 使用指定的账户对数据进行签名，该账户必须先解锁
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. data： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. hexstr： 账本名称
        - 4. text:
        @return:
        - 1. 签名结果字符串
        """
        #好像有点问题


    def test_call(self):
        """
        @describe: 获取指定块中特定账户地址的余额
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块中特定账户地址的余额,int
        """
        #好像有点问题


    def test_estimateGas(self):
        """
        @describe: 估算交易的gas用量
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 模拟调用的gas用量，
        """
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce + 1,
            "data": '',
            "chainId": chain_id,
            "value": 1,
        }
        print(platone.estimateGas(transaction_dict, ledger=sys_ledger))

class TestPersonal():

    def test_importRawKey(self):
        """
        @describe: 导入私钥到钱包
        @parameters:
        - 1. private_key： 私钥
        - 2. passphrase： 密码
        @return:
        - 1. address: 钱包地址
        """
        import_sesult = personal.importRawKey(node_admin_private_key, '12345678')
        assert import_sesult == node_admin_address
        accounts_list = personal.listAccounts
        assert node_admin_address in accounts_list


    def test_newAccount(self):
        """
        @describe: 创建一个钱包
        @parameters:
        - 1. password： 密码
        @return:
        - 1. address: 钱包地址
        """
        newaccount = personal.newAccount('12345678')
        accounts_list = personal.listAccounts
        assert newaccount in accounts_list


    def test_listAccounts(self):
        """
        @describe: 查询地址列表
        @parameters:
        - 1. password： none
        @return:
        - 1. address_list: 钱包地址列表
        """
        accounts_list = personal.listAccounts
        assert isinstance(accounts_list, list)


    def test_listWallets(self):
        """
        @describe: 查询钱包文件信息列表
        @parameters:
        - 1. password： none
        @return:
        - 1. address_list: 钱包文件信息列表
        """
        wallets_list = personal.listWallets
        print(wallets_list)
        assert isinstance(wallets_list, list)


    def test_sendTransaction(self):
        """
        todo: 没有调通
        @describe: 发送交易
        @parameters:
        - 1. transaction_dict： 交易信息
        - 2. passphrase：密码
        - 3. ledger： 账本名称
        @return:
        - 1.
        """
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": chain_id,
            "value": 1,
        }
        print(personal.sendTransaction(transaction_dict, '12345678', sys_ledger))


    def test_lockAccount(self):
        """
        @describe: 锁钱包地址
        @parameters:
        - 1. account： 钱包地址
        @return:
        - 1. bool
        """
        assert personal.lockAccount(main_address)


    def test_unlockAccount(self):
        """
        @describe: 锁钱包地址
        @parameters:
        - 1. account： 钱包地址
        - 2. passphrase： 密码
        - 3. duration： 时间戳
        @return:
        - 1. bool
        """
        assert personal.unlockAccount(main_address, '12345678')


    def test_sign(self):
        """
        todo: 什么情况是需要签名的
        @describe:
        @parameters:
        - 1. message：
        - 2. signer：
        - 3. passphrase：
        - 4. ledger:
        @return:
        - 1.
        """
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce + 1,
            "data": '',
            "chainId": chain_id,
            "value": 1,
        }
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=w3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        tx_hash = HexBytes(platone.sendRawTransaction(data, ledger)).hex()
        print(personal.sign(data, main_private_key, '12345678'))


    def test_signTransaction(self):
        """
        @describe: 调用签名指定交易，不广播到网络中。 签名后的交易可以在稍后
        @parameters:
        - 1. transaction_dict： 交易信息
        - 2. passphrase：密码
        - 3. ledger: 账本
        @return:
        - 1. 已签名交易对象
            - 1.1. raw：已签名的编码的交易
            - 1.2  tx：原始交易对象
        """
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            'from': main_address,
            "to": user_address,
            "gasPrice": hex(platone.gasPrice(sys_ledger)),
            "gas": hex(21000),
            "nonce": hex(nonce),
            "data": '',
            "chainId": hex(chain_id),
            "value": hex(1 * 10 ** 18),
        }
        result = personal.signTransaction(transaction_dict, '12345678', ledger=sys_ledger)
        assert result['raw'][:2] == '0x'


    def test_ecRecover(self):
        """
        todo: 不会
        @describe: 从签名中提取签名私钥对应的钱包地址
        @parameters:
        - 1. transaction_dict： 交易信息
        - 2. passphrase：密码
        - 3. ledger: 账本
        @return:
        - 1. 已签名交易对象
            - 1.1. raw：已签名的编码的交易
            - 1.2  tx：原始交易对象
        """
        pass


    def test_openWallet(self):
        """
        @describe:
        @parameters:
        - 1. transaction_dict： 交易信息
        - 2. passphrase：密码
        - 3. ledger: 账本
        @return:
        - 1. 已签名交易对象
            - 1.1. raw：已签名的编码的交易
            - 1.2  tx：原始交易对象
        """
        newaccount = personal.newAccount('12345678')
        url = personal.listWallets[0]['url']
        result = personal.openWallet(url, '12345678')
        assert result is None



class TestUser():


    def test_add_chain_admin(self):
        address = chain_admin_address
        name = '链管理员'
        mobile = '18665851938'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 4611686018427387904
        private_key = main_private_key
        result = user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)

    def test_add_node_admin(self):
        address = node_admin_address
        name = '节点管理员'
        mobile = '18665851938'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 2305843009213693952
        private_key = main_private_key
        result = user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)

    def test_add_contract_admin(self):
        address = contract_admin_address
        name = '合约管理员'
        mobile = '18665851938'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 1152921504606846976
        private_key = main_private_key
        result = user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)

    def test_add_contract_deployer(self):
        address = contract_deployer_address
        name = '合约部署者'
        mobile = '18665851938'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 576460752303423488
        private_key = main_private_key
        result = user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)
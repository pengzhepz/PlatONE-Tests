import hexbytes

from cases.ledger.conftest import *


class TestPlatone():


    def test_protocolVersion(self, client):
        """
        @describe: 获取当前以太坊协议的版本
        @parameters:
        - 1. null
        @return:
        - 1. 当前以太坊协议的版本,String
        """
        version = client.platone.protocolVersion
        assert version == '63'


    def test_syncing(self, client):
        """
        @describe: 检查节点当前是否已经与网络同步
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. Object或Bool。
        """
        result = client.platone.syncing(sys_ledger)
        assert isinstance(result, bool)


    def test_gasPrice(self, client):
        """
        @describe: 获取当前gas价格，该价格由最近的若干块的gas价格中值决定。
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. 当前gas价格,int
        """
        gasPrice = client.platone.gasPrice(sys_ledger)
        assert gasPrice == 1000000000


    def test_accounts(self, client):
        """
        @describe: 获取当前节点控制的账户列表
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. 返回当前节点控制的账户列表,list
        """
        new_account = client.personal.newAccount('12345678')
        accounts = client.platone.accounts(sys_ledger)
        assert isinstance(accounts, list)
        assert new_account in accounts


    def test_blockNumber(self, client):
        """
        @describe: 获取当前块编号
        @parameters:
        - 1. ledger: 账本名称
        @return:
        - 1. 返回当前块编号,int
        """
        blocknumber = client.platone.blockNumber(sys_ledger)
        assert isinstance(blocknumber, int) and blocknumber >= 0


    def test_evidences(self, client):
        # sdk装饰器要是没有注释记得注释
        """
        @describe: 获取账户地址指定位置的存储内容
        @parameters:
        - 1. account： ledger： 账本名称
        @return:
        - 1. 账户地址指定位置的存储内容,AttributeDict
        """
        evidences = client.platone.evidences(sys_ledger)
        assert isinstance(evidences, dict)

    def test_consensusStatus(self, client):
        # sdk装饰器要是没有注释记得注释
        """
        @describe: 获取当前节点所在区块树的共识状态信息
        @parameters:
        - 1. ledger： 账本名称
        @return:
        - 1. 当前节点所在区块树的共识状态信息,AttributeDict
        """
        status_info = client.platone.consensusStatus(sys_ledger)
        blochnumber = status_info['blockTree']['root']['blockNumber']
        assert 0 <= client.platone.blockNumber(sys_ledger) - blochnumber <= 3


    def test_getPrepareQC(self, transfer_info):
        """
        @describe: 获取指定块高的信息
        @parameters:
        - 1. block_number： 块高
        - 2. ledger： 账本名称
        @return:
        - 1. 指定块高的信息,AttributeDict
        """
        client = transfer_info
        prepare = client.platone.getPrepareQC(client.block_identifier, sys_ledger)
        prepare_blocknumber = prepare['blockNumber']
        assert prepare_blocknumber == client.block_identifier


    def test_getbalance(self, client):
        """
        @describe: 获取指定块中特定账户地址的余额
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块中特定账户地址的余额,int
        """
        balance = client.platone.getBalance(main_address, ledger=sys_ledger)
        assert isinstance(balance, int) and balance >= 0


    def test_getStorageAt(self, transfer_info):
        """
        @describe: 获取一个地址的指定位置存储内容
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. position： 存储中的索引编号, Number
        - 3. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 4. ledger:  账本名称
        @return:
        - 1. 一个地址的指定位置存储内容
        """
        client = transfer_info
        storage = client.platone.getStorageAt(main_address, 0, transfer_info.block_identifier, ledger=sys_ledger)
        assert isinstance(storage, HexBytes)


    def test_getCode(self, client):
        """
        todo: 前置需要布合约
        @describe: 获取指定合约地址处的二进制代码
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 指定地址处的代码
        """
        code = client.platone.getCode(main_address, ledger=sys_ledger)
        print(code)
        assert isinstance(code, HexBytes)


    def test_getBlock(self, client):
        """
        todo: 调不通
        @describe: 获取指定块编号或块哈希对应的块
        @parameters:
        - 1. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 2. full_transactions: Boolean -  可选，默认值为false。当设置为true时,返回块中将包括所有交易详情，否则仅返回交易哈希
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块编号或块哈希对应的块
        """
        # block = client.platone.getBlock(hex(1), ledger=sys_ledger)
        block = client.platone.getBlock("latest", ledger=sys_ledger)
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
        client = transfer_info
        count = client.platone.getBlockTransactionCount(client.block_identifier, sys_ledger)
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
        client = transfer_info
        result = client.platone.getTransaction(client.transaction_hash.hex(), sys_ledger)
        assert result['hash'] == client.transaction_hash and result['blockNumber'] == client.block_identifier


    def test_getRawTransaction(self, transfer_info):
        """
        @describe: 获取具有指定哈希值的交易对象HexBytes 值
        @parameters:
        - 1. transaction_hash： 要查询的交易的哈希值
        - 2. ledger： 账本名称
        @return:
        - 1. 具有指定哈希值的交易对象HexBytes 值,
        """
        client = transfer_info
        raw_transaction = client.platone.getRawTransaction(client.transaction_hash.hex(), sys_ledger)
        assert raw_transaction[:2] == '0x' and len(raw_transaction) == 224


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
        client = transfer_info
        block = client.platone.getTransactionFromBlock(client.block_identifier, client.transaction_index, sys_ledger)
        assert client.transaction_hash == block['hash']


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
        client = transfer_info
        block = client.platone.getTransactionByBlock(client.block_identifier, client.transaction_index, sys_ledger)
        assert client.transaction_hash == block['hash']


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
        client = transfer_info
        receipt = client.platone.waitForTransactionReceipt(client.transaction_hash.hex(), sys_ledger, 120)
        assert receipt == client.transaction_receipt


    def test_getTransactionReceipt(self, transfer_info):
        """
        @describe: 指定交易的收据对象。如果交易处于pending状态，则返回null
        @parameters:
        - 1. transaction_hash： 交易的哈希值 -String
        - 2. ledger： 账本名称
        @return:
        - 1. 指定交易的收据对象。如果交易处于pending状态，则返回null
        """
        client = transfer_info
        receipt = client.platone.getTransactionReceipt(client.transaction_hash.hex(), sys_ledger)
        assert receipt == client.transaction_receipt
        transaction_hash1 = '123'
        receipt1 = client.platone.getTransactionReceipt(transaction_hash1, sys_ledger)
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
        client = transfer_info
        count = client.platone.getTransactionCount(main_address, client.block_identifier, sys_ledger)
        transaction = transfer(main_private_key, user_address, 1 * 10 ** 18, sys_ledger, client)
        block = transaction['blockNumber']
        count1 = client.platone.getTransactionCount(main_address, block, sys_ledger)
        assert count1 - 1 == count



    def test_replaceTransaction(self, client):
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
        platone = client.platone
        txpool = client.txpool
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce + 1,
            "data": '',
            "chainId": client.chain_id,
            "value": 1,
        }
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        demo = platone.sendRawTransaction(data, sys_ledger)
        tx_hash = HexBytes(platone.sendRawTransaction(data, sys_ledger)).hex()
        print(tx_hash)
        print(txpool.content(sys_ledger))

        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger) + 1,
            "gas": 21000 * 2,
            "nonce": nonce,
            "data": '123',
            "chainId": client.chain_id,
            "value": 1 * 10 ** 18,
        }
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        # balance = platone.replaceTransaction(tx_hash, data, sys_ledger)
        balance = platone.replaceTransaction(demo, data, sys_ledger)
        print(balance)
        print(txpool.content(sys_ledger))


    def test_modifyTransaction(self, client):
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
        transaction_hash = ''
        balance = client.platone.modifyTransaction(transaction_hash)

    def test_sendTransaction(self, client):
        """
        todo:有问题需要星哥改sdk
        @describe: 向platone 链上提交一个交易
        @parameters:
        - 1. transaction： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. ledger： 账本名称
        @return:
        - 1. 32字节长的交易哈希值?
        """
        platone = client.platone
        from_address = Account.privateKeyToAccount(main_private_key, hrp, mode='SM').address
        nonce = platone.getTransactionCount(from_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": hex(platone.gasPrice(sys_ledger)),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": client.chain_id,
            "value": 1 * 10 ** 18,
        }
        balance = platone.sendTransaction(transaction_dict, sys_ledger)
        print(balance)


    def test_sendRawTransaction(self, client):
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
        platone = client.platone
        from_address = Account.privateKeyToAccount(main_private_key, hrp, mode='SM').address
        nonce = platone.getTransactionCount(from_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": client.chain_id,
            "value": 1 * 10 ** 18,
        }
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        tx_hash = platone.sendRawTransaction(data, sys_ledger)
        print(type(tx_hash))
        assert isinstance(tx_hash, HexBytes)


    def test_sign(self, client):
        """
        todo：调不通
        @describe: 使用指定的账户对数据进行签名，该账户必须先解锁
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. data： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. hexstr： 账本名称
        - 4. text:
        @return:
        - 1. 签名结果字符串
        """
        newaccount = client.personal.newAccount('12345678')
        client.personal.unlockAccount(newaccount, '12345678')
        result = client.platone.sign(newaccount, text='xx')
        assert isinstance(result, hexbytes.main.HexBytes)

    def test_call(self, client):
        """
        todo: 调不通
        @describe: 获取指定块中特定账户地址的余额
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 指定块中特定账户地址的余额,int
        """
        #好像有点问题
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "from": main_address,
            "to": user_address,
            "gasPrice": client.platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": client.chain_id,
            "value": 1,
        }
        result = client.platone.call(transaction_dict)
        print(result)


    def test_estimateGas(self, client):
        """
        @describe: 估算交易的gas用量
        @parameters:
        - 1. account： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
        - 2. block_identifier： 整数块编号，或者字符串"latest", "earliest" 或 "pending"
        - 3. ledger： 账本名称
        @return:
        - 1. 模拟调用的gas用量，
        """
        transaction_dict = {}
        estimateGas = client.platone.estimateGas(transaction_dict, ledger=sys_ledger)
        assert estimateGas == 53000

    def test_filter(self, client):
        """
        @describe: 用来监听合约事件
        @parameters:
        - 1. filter_params：
        - 2. filter_id：
        - 3. ledger： 账本名称
        @return:
        - 1.
        """
        filter = client.platone.filter(filter_params = 'latest')
        callbacks = client.platone.filter(filter_params ='latest').callbacks
        assert callbacks == []

    def test_getFilterChanges(self, client):
        """
        todo: 调不通
        @describe: 用来轮询指定的过滤器，并返回自上次轮询之后新产生的日志数组
        @parameters:
        - 1. filter_params：
        - 2. filter_id：
        - 3. ledger： 账本名称
        @return: 返回一个数组，成员类型按过滤器不同有所区别：
            对于使用eth_newBlockFilter创建的过滤器，返回区块哈希，例如： ["0x3454645634534..."]
            对于使用eth_newPendingTransactionFilter创建的过滤器，返回交易哈希，例如： ["0x6345343454645..."]
            对于使用eth_newFilter创建的过滤器，返回日志对象，结构如下：
            removed: 日志是否已删除
            logIndex: 日志在区块内的索引
            transactionIndex: 产生日志的交易索引
            transactionHash: 产生日志的交易哈希
            blockHash: 日志所在区块的哈希
            blockNumber: 日志所在区块号
            address: 产生日志的源地址
            data: 日志的非索引参数
            topics:日志的主题数组
        """
        filter_id = client.web3.manager.request_blocking(
            "platon_newBlockFilter", client.platone.set_ledger([], sys_ledger),
        )
        filter = client.platone.getFilterChanges(filter_id, sys_ledger)
        print(filter_id)
        print(filter)


    def test_getFilterLogs(self, client):
        """
        todo: 为什么调不通啊
        @describe: 指定过滤器的日志数组
        @parameters:
        - 1. filter_id：
        - 2. ledger： 账本名称
        @return:
        - 1. 指定过滤器的日志数组
        """
        filter = client.platone.filter(filter_params='latest')
        filter_id = client.web3.manager.request_blocking(
            "platon_newBlockFilter", client.platone.set_ledger([], sys_ledger),
        )
        logs = client.platone.getFilterLogs(filter_id, sys_ledger)
        print(logs)


    def test_getLogs(self, client):
        """
        todo: 调不通
        @describe: 匹配指定过滤器对象的日志数组
        @parameters:
        - 1. filter_params：
        - 2. ledger： 账本名称
        @return:
        - 1. 匹配指定过滤器对象的日志数组
        """
        logs = client.platone.getLogs('latest', sys_ledger)
        print(logs)


    def test_uninstallFilter(self, client):
        """
        todo: {'error': {'code': -32602, 'message': 'too many arguments, want at most 1'}
        @describe: 指定过滤器的日志数组
        @parameters:
        - 1. filter_id：
        - 2. ledger： 账本名称
        @return:
        - 1. 指定过滤器的日志数组
        """
        filter = client.platone.filter(filter_params='latest')
        filter_id = client.web3.manager.request_blocking(
            "platon_newBlockFilter", client.platone.set_ledger([], sys_ledger),
        )
        logs = client.platone.uninstallFilter(filter_id, sys_ledger)
        print(logs)


    def test_wasm_type(self, client):
        #只是更改合约信息
        abi_data = ''
        client.platone.wasm_type(abi_data)
        pass


    def test_contract(self, client):
        """
        @describe: 简化了与以太坊区块链上智能合约的交互。创建合约对象时， 只需指定相应智能合约的json接口，web3就可以自动地将所有的调用转换为底层 基于RPC的ABI调用
        @parameters:
        - 1. jsonInterface ： 要实例化的合约的json接口
        - 2. address： 地址
        @return:
        - 1. 合约实例及其所有方法和事件
        """
        ABI = [{"constant":False,"inputs":[{"internalType":"string","name":"ledgerJson","type":"string"}],"name":"CreateLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"GetAllLedgers","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"string","name":"ledgerName","type":"string"},{"internalType":"string","name":"nodeID","type":"string"},{"internalType":"string","name":"blsPubKey","type":"string"}],"name":"JoinLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"string","name":"nodeID","type":"string"}],"name":"JoinedLedgers","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"string","name":"ledgerName","type":"string"},{"internalType":"string","name":"nodeID","type":"string"}],"name":"QuitLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"string","name":"ledgerName","type":"string"}],"name":"TerminateLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"}]
        contract = client.platone.contract(address=client.web3.ledger_manager_address, abi=ABI, ledger=sys_ledger)
        assert contract
        res = contract.functions.GetAllLedgers().call()
        assert_code(json.loads(res[0]), 0)


    def test_wasmcontract(self, client):
        """
        @describe: 简化了与以太坊区块链上智能合约的交互。创建合约对象时， 只需指定相应智能合约的json接口，web3就可以自动地将所有的调用转换为底层 基于RPC的ABI调用
        @parameters:
        - 1. jsonInterface ： 要实例化的合约的json接口
        - 2. address： 地址
        @return:
        - 1. 合约实例及其所有方法和事件
        """
        ABI = [{"constant":False,"inputs":[{"internalType":"string","name":"ledgerJson","type":"string"}],"name":"CreateLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"GetAllLedgers","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"string","name":"ledgerName","type":"string"},{"internalType":"string","name":"nodeID","type":"string"},{"internalType":"string","name":"blsPubKey","type":"string"}],"name":"JoinLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"string","name":"nodeID","type":"string"}],"name":"JoinedLedgers","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"string","name":"ledgerName","type":"string"},{"internalType":"string","name":"nodeID","type":"string"}],"name":"QuitLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"string","name":"ledgerName","type":"string"}],"name":"TerminateLedger","outputs":[{"internalType":"int32","name":"","type":"int32"}],"payable":False,"stateMutability":"nonpayable","type":"function"}]
        contract = client.platone.contract(address=client.web3.ledger_manager_address, abi=ABI, ledger=sys_ledger)
        assert contract
        res = contract.functions.GetAllLedgers().call()
        assert_code(json.loads(res[0]), 0)


    def test_setContractFactory(self, client):
        """
        todo: 待验证
        @describe:
        @parameters:
        - 1. jsonInterface ：
        - 2. address：
        @return:
        - 1.
        """
        contractFactory = ''
        client.platone.setContractFactory(contractFactory)
        pass

    def test_generateGasPrice(self, client):
        """
        @describe: 产生的GasPrice
        @parameters:
        - 1. transaction_params:交易信息
        @return:
        - 1. wei为单位的gas price数值
        """
        transaction_dict = {
            # "to": to_address,
            # "gasPrice": platone.gasPrice(ledger),
            # "gas": 21000,
            # "nonce": nonce,
            # "data": '',
            # "chainId": chain_id,
            # "value": amount,
        }
        gasprice = client.platone.generateGasPrice(transaction_dict)
        assert gasprice is None


    def test_setGasPriceStrategy(self, client):
        """
        @describe:设定选定的gas price 策略
        @parameters:
        - 1. gas_price_strategy ：一种签名的方法
        @return:
        - 1.以wei为单位的gas price数值
        """
        gas_price_strategy = ''
        gasprice = client.platone.setGasPriceStrategy(gas_price_strategy)
        assert gasprice is None


    def test_analyzeReceiptByHash(self, transfer_info):
        """
        todo: IndexError: list index out of range
        @describe:
        @parameters:
        - 1. jsonInterface ：
        - 2. address：
        @return:
        - 1.
        """
        client = transfer_info
        platone = client.platone
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": 200,
            "value": 1,
        }
        logger.info(f'transaction_dict: {transaction_dict}')
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        tx_hash = HexBytes(platone.sendRawTransaction(data, sys_ledger)).hex()
        print(platone.analyzeReceiptByHash(tx_hash, sys_ledger))


    def test_analyzeReceipt(self, client):
        """
        todo: IndexError: list index out of range
        @describe:
        @parameters:
        - 1. jsonInterface ：
        - 2. address：
        @return:
        - 1.
        """
        platone = client.platone
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": client.chain_id,
            "value": 1,
        }
        logger.info(f'transaction_dict: {transaction_dict}')
        signedTransactionDict = platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        )
        data = signedTransactionDict.rawTransaction
        tx_hash = HexBytes(platone.sendRawTransaction(data, sys_ledger)).hex()
        result = platone.waitForTransactionReceipt(tx_hash, sys_ledger)
        print(platone.analyzeReceipt(result))


    def test_ecrecover(self, client):
        """
        todo: block_identifier填什么
        @describe:
        @parameters:
        - 1. jsonInterface ：
        - 2. address：
        @return:
        - 1.
        """
        result = client.platone.ecrecover("latest")
        # pass
        print(result)

class TestPersonal():

    def test_importRawKey(self, client):
        """
        @describe: 导入私钥到钱包
        @parameters:
        - 1. private_key： 私钥
        - 2. passphrase： 密码
        @return:
        - 1. address: 钱包地址
        """
        import_sesult = client.personal.importRawKey(node_admin_private_key, '12345678')
        assert import_sesult == node_admin_address
        accounts_list = client.personal.listAccounts
        assert node_admin_address in accounts_list



    def test_newAccount(self, client):
        """
        @describe: 创建一个钱包
        @parameters:
        - 1. password： 密码
        @return:
        - 1. address: 钱包地址
        """
        newaccount = client.personal.newAccount('12345678')
        accounts_list = client.personal.listAccounts
        assert newaccount in accounts_list


    def test_listAccounts(self, client):
        """
        @describe: 查询地址列表
        @parameters:
        - 1. password： none
        @return:
        - 1. address_list: 钱包地址列表
        """
        accounts_list = client.personal.listAccounts
        print(accounts_list)
        assert isinstance(accounts_list, list)


    def test_listWallets(self, client):
        """
        @describe: 查询钱包文件信息列表
        @parameters:
        - 1. password： none
        @return:
        - 1. address_list: 钱包文件信息列表
        """
        wallets_list = client.personal.listWallets
        print(wallets_list)
        assert isinstance(wallets_list, list)


    def test_sendTransaction(self, client):
        """
        todo: 没有调通   ValueError: too many values to unpack (expected 3)
        @describe: 发送交易
        @parameters:
        - 1. transaction_dict： 交易信息
        - 2. passphrase：密码
        - 3. ledger： 账本名称
        @return:
        - 1.
        """
        platone = client.platone
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": client.chain_id,
            "value": 1,
        }
        print(client.personal.sendTransaction(transaction_dict, '12345678', sys_ledger))


    def test_lockAccount(self, client):
        """
        @describe: 锁钱包地址
        @parameters:
        - 1. account： 钱包地址
        @return:
        - 1. bool
        """
        newaccount = client.personal.newAccount('12345678')
        assert client.personal.lockAccount(newaccount)


    def test_unlockAccount(self, client):
        """
        @describe: 锁钱包地址
        @parameters:
        - 1. account： 钱包地址
        - 2. passphrase： 密码
        - 3. duration： 时间戳
        @return:
        - 1. bool
        """
        newaccount = client.personal.newAccount('12345678')
        assert client.personal.unlockAccount(newaccount, '12345678')



    def test_put_into_keystore_unlockaccount(self, client):
        # bug19610已测
        client.put_wallet_file()
        time.sleep(5)
        result = client.personal.unlockAccount('lax1nhst6nsexls7dsmshhk6crg2e2t2cduqseczvd', '12345678')
        assert result



    def test_sign(self, client):
        """
        todo: 什么情况是需要签名的。 TypeError: Could not encode to JSON: dict had unencodable value at keys: {'params': because (list had unencodable value at index: [0: because (Object of type module is not JSON serializable)])}
        @describe:
        @parameters:
        - 1. message：
        - 2. signer：
        - 3. passphrase：
        - 4. ledger:
        @return:
        - 1.
        """
        platone = client.platone
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce + 1,
            "data": '',
            "chainId": client.chain_id,
            "value": 1,
        }
        # signedTransactionDict = platone.account.signTransaction(
        #     transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        # )
        # data = signedTransactionDict.rawTransaction
        # tx_hash = HexBytes(platone.sendRawTransaction(data, ledger)).hex()
        # client.personal.importRawKey(main_private_key, "12345678")
        client.personal.unlockAccount(main_address, '123456')
        print(client.personal.sign(transaction_dict, main_address, '12345678'))


    def test_signTransaction(self, client):
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
        platone = client.platone
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            # 'from': main_address,
            "to": user_address,
            "gasPrice": hex(platone.gasPrice(sys_ledger)),
            "gas": hex(21000),
            "nonce": hex(nonce),
            "data": '',
            "chainId": hex(client.chain_id),
            "value": hex(1 * 10 ** 18),
        }
        try:
            client.personal.importRawKey(main_private_key, "12345678")
        except:
            pass
        client.personal.unlockAccount(main_address, '123456')
        result = client.personal.signTransaction('transaction_dict', '12345678', ledger=sys_ledger)
        assert result['raw'][:2] == '0x'


    def test_ecRecover(self, client):
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
        nonce = client.platone.getTransactionCount(main_address, ledger=sys_ledger)
        transaction_dict = {
            "to": user_address,
            "gasPrice": client.platone.gasPrice(sys_ledger),
            "gas": 21000,
            "nonce": nonce,
            "data": '',
            "chainId": client.chain_id,
            "value": 1 * 10 ** 18,
        }
        signedTransactionDict = client.platone.account.signTransaction(
            transaction_dict, main_private_key, net_type=client.web3.net_type, mode='SM'
        )
        # data = signedTransactionDict.rawTransaction
        # tx_hash = HexBytes(client.platone.sendRawTransaction(data, sys_ledger)).hex()
        # transaction_receipt = client.platone.waitForTransactionReceipt(tx_hash, sys_ledger)
        signature = transaction_dict
        result = client.personal.ecRecover('hello', signature)
        print(result)


    def test_openWallet(self, client):
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
        newaccount = client.personal.newAccount('12345678')
        url = client.personal.listWallets[0]['url']
        result = client.personal.openWallet(url, '12345678')
        assert result is None


@pytest.mark.skip(reason='环境重置有，不重复测')
class TestUser():

    def test_add_chain_admin(self, client):
        address = chain_admin_address
        name = '链管理员'
        mobile = '16675161604'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 4611686018427387904
        private_key = main_private_key
        result = client.user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)

    def test_add_node_admin(self, client):
        address = node_admin_address
        name = '节点管理员'
        mobile = '16675161604'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 2305843009213693952
        private_key = main_private_key
        result = client.user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)

    def test_add_contract_admin(self, client):
        address = contract_admin_address
        name = '合约管理员'
        mobile = '16675161604'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 1152921504606846976
        private_key = main_private_key
        result = client.user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)

    def test_add_contract_deployer(self, client):
        address = contract_deployer_address
        name = '合约部署者'
        mobile = '16675161604'
        email = '64216398@qq.com'
        desc = 'node'
        roles = 576460752303423488
        private_key = main_private_key
        result = client.user.add(address, name, mobile, email, desc, roles, private_key)
        assert_code(result, 0)



class TestNode():


    def test_listAll(self, client):
        print(client.node.listAll())



class TestParam():


    def test_getSystemParameter(self, client):
        sys_parameter = client.param.getSystemParameter()
        assert isinstance(sys_parameter, list)
        assert json.loads(sys_parameter[0])['code'] == 0



    def test_enableDeploy(self, client):
        #todo: 加断言
        result = client.param.enableDeploy(main_private_key)
        print(result)
        result1 = client.param.disableDeploy(main_private_key)
        print(result1)




    def test_updateBlockGasLimit(self, client):
        # 多账本功能不涉及，此版本不测
        pass
        # client.param.updateBlockGasLimit()


    def test_updateIsProduceEmptyBlock(self,client):
        update_result = client.param.updateIsProduceEmptyBlock(False, main_private_key)
        assert_code(update_result, 0)
        update_result = client.param.updateIsProduceEmptyBlock(True, main_private_key)
        assert_code(update_result, 0)


    def test_updateIsTxUseGas(self, client):
        #todo: 设置成需不需要都不需要gas呀
        result = client.param.updateIsTxUseGas(False, main_private_key)
        print(result)
        time.sleep(3)
        balance = client.platone.getBalance(main_address, ledger=sys_ledger)
        result_tr = transfer(main_private_key, user_address, 1, sys_ledger, client)
        print(result_tr)
        time.sleep(3)
        balance_after = client.platone.getBalance(main_address, ledger=sys_ledger)
        print(balance, balance_after)

        result_true = client.param.updateIsTxUseGas(True, main_private_key)
        print(result_true)
        time.sleep(3)
        balance_true_befor = client.platone.getBalance(main_address, ledger=sys_ledger)
        result_tr1 = transfer(main_private_key, user_address, 1, sys_ledger, client)
        print(result_tr1)
        time.sleep(3)
        balance_true_after = client.platone.getBalance(main_address, ledger=sys_ledger)
        print(balance_true_befor, balance_true_after)


    def test_updateTxGasLimit(self, client):
        #todo: 'code': 303001, 'code_info': 'parameter error'
        update_result = client.param.updateTxGasLimit(10000, main_private_key)
        print(update_result)

    def test_updateSystemParameter(self, client):
        # 与多账本无关，此版本不测
        # update_result = client.param.updateSystemParameter()
        pass



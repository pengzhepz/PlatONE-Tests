import pytest
from loguru import logger
from setting import LOG_DIR, LOG_SIZE


@pytest.fixture(scope='session', autouse=False)
def global_evn(request):
    logger.add(LOG_DIR, rotation=LOG_SIZE)
    logger.info('>> Test start! >>>>>>>>>>>>>>')
    evn = None  # todo：部署环境
    return evn


@pytest.fixture(scope='session', autouse=False)
def init_node(global_evn):
    # 获取初始验证节点
    return global_evn.init_node  # todo：具体实现


def random_node(global_evn):
    # 获取随机节点
    return global_evn.init_node  # todo：具体实现

@pytest.fixture()
def verifier_node(global_evn):
    # 查询并获取验证节点
    pass


@pytest.fixture()
def normal_node(global_evn):
    # 查询并获取普通节点
    pass




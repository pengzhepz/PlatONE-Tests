from selenium.webdriver.common.by import By


class NodeMangerLocator:

    """
    TODO： 缺少修改节点
    """

    add_node = (By.CLASS_NAME,'anticon-plus')
    node_name = (By.ID,'normal_login_name')
    node_desc = (By.ID,'normal_login_desc')
    node_rpc = (By.ID,'normal_login_rpcPort')
    docker_choice = (By.CLASS_NAME,'ant-select-arrow')
    license = (By.CLASS_NAME,'ant-input-search-button')
    server_ip = (By.ID,'normal_login_ip')
    server_pwd = (By.ID,'normal_login_password')
    node_type = (By.XPATH,'//*[@id="normal_login"]/div[1]/div[2]/div/div[2]/div/div/div/span')
    node_host = (By.ID,'normal_login_hostAddress')
    node_p2pport = (By.ID,'normal_login_p2pPort')
    genesis_file = (By.XPATH,'//*[@id="normal_login"]/div[4]/div[1]/div[2]/div/div[2]/div/div/span/span/span/button')
    node_script = (By.ID,'normal_login_scriptPath')
    server_user = (By.ID,'normal_login_userName')
    submit = (By.XPATH,'//*[@id="normal_login"]/div[5]/button')

    # 节点操作
    edit_btn = (By.XPATH, '//*[text()="修改"]')
    edit_public_btn = (By.XPATH, '//*[text()="修改为共识节点"]')
    stop_btn = (By.XPATH, '//*[text()="禁用"]')
    delete_btn = (By.XPATH, '//*[text()="删除"]')


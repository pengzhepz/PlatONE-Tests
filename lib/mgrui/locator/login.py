from selenium.webdriver.common.by import By


class LoginLocator:
    # 元素locator
    # 登录页面
    select_user = (By.CLASS_NAME, 'select_btn')
    username_input = (By.ID, 'normal_login_username')
    password_input = (By.ID, 'normal_login_password')
    authcode_input = (By.CLASS_NAME, 'ant-select-selection-item')
    refresh_authcode_button = (By.CLASS_NAME, 'ant-select-arrow')
    select_auth = (By.CLASS_NAME,'ant-select-selector')
    login_button = (By.CLASS_NAME, 'login-form-button')
    logout = (By.CLASS_NAME,'avatar')
    logout_2 = (By.XPATH,'/html/body/div[3]/div/div/ul/li/a')

    # 配置链
    register_btn = (By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/p[1]/span')
    create_btn = (By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/p[2]/span')
    set_chain = (By.CLASS_NAME, 'chain_btn')
    ip_address = (By.ID, 'connent_box_ip')
    rpc_port = (By.ID, 'connent_box_port')
    connect_chain = (By.CLASS_NAME, 'connent_box_button')

    # 创建钱包
    create_chain = (By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/span')
    wallet_pwd = (By.ID, 'walletForm_password')
    wallet_pwd_2 = (By.ID, 'walletForm_checkPassword')
    confirm_create_wallet = (By.CLASS_NAME,'submit_btn')
    # close_window = (By.XPATH,'//*[@id="root"]/div/div/div[3]/div[2]/div/div[2]/button')
    copy_address = (By.ID,'copy_text')
    download_json = (By.XPATH,'//*[@id="root"]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[2]/button[2]')
    next_step = (By.XPATH,'//*[@id="root"]/div/div/div[3]/div[2]/div/div[2]/div[2]/div/div[3]/button/span')

    # 链数据
    script_path = (By.ID,'chainForm_scriptPath')
    nodeIp = (By.ID,'chainForm_nodeIp')
    chain_rpc = (By.ID,'chainForm_rpcPort')
    license = (By.XPATH,'ant-input-search-button')
    useDock = (By.CLASS_NAME,'ant-select-selection-item')
    chain_user = (By.ID,'chainForm_userName')
    genesis_address = (By.ID,'chainForm_creatorAddress')
    desc = (By.ID,'chainForm_nodeDesc')
    nodep2p = (By.ID,'chainForm_p2pPort')
    server_ip = (By.ID,'chainForm_serverIp')
    chain_pwd = (By.ID,'chainForm_password')
    start_create_chain = (By.XPATH,'//*[@id="chainForm"]/div[7]/button')

    # 注册用户
    normal_user = (By.ID,'normal_login_userName')
    nuser_pwd = (By.ID,'normal_login_password')
    nuser_pwd2 = (By.ID,'normal_login_checkPassword')
    user_phone = (By.ID,'normal_login_phone')
    register_nuser = (By.XPATH,'//*[@id="normal_login"]/div[7]/button')

    # 检查locator
    login_errormsg_txt = (By.XPATH, '/html/body/div[2]')
    username_warningmsg_txt = (By.XPATH, '//*[@id="app"]/div/form/div[2]/div/div[2]')
    password_warningmsg_txt = (By.XPATH, '//*[@id="app"]/div/form/div[3]/div/div[2]')
    authcode_warningmsg_txt = (By.XPATH, '//*[@id="app"]/div/form/div[4]/div/div[2]')
    title_txt = (By.XPATH, '//*[@id="app"]/div/form/div[1]/h1')  # 退出登录后回到登录页面的检查点--财务系统标题
    no_auth = (By.XPATH,'//*[text()="不使用国密"]')
    user_id = (By.XPATH,'//*[@id="root"]/div/section/section/div/div/main/div/div/div/div[2]/div[1]/div[4]')

from selenium.webdriver.common.by import By


class UserMangerLocator:
    add_user = (By.CLASS_NAME, 'anticon-plus')
    name = (By.ID, 'normal_login_name')
    phone = (By.ID, 'normal_login_mobile')
    email = (By.ID, 'normal_login_email')
    address = (By.ID, 'normal_login_address')
    power = (By.CLASS_NAME, 'ant-select-selection-item')
    submit_btn = (By.CLASS_NAME, 'submit_btn')

from selenium.webdriver.common.by import By


class BiilMangerLocator:

    add_bill = (By.CLASS_NAME,'anticon-plus')
    bill_name = (By.ID,'normal_login_ledgerName')
    add_bill_node = (By.XPATH,'//*[@id="normal_login_nodes"]/div/div/table/tbody/tr/td[3]/div')
    submit = (By.CLASS_NAME,'submit_btn')

    add_sub_node = (By.XPATH,'//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]/div/div[1]/span/span')
    closs_bill_node = (By.XPATH,'//*[@id="root"]/div/section/section/div/div/main/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]/div/div[2]/span/span')

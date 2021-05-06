import datetime
import time
from typing import List
from loguru import logger
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from setting import IMAGE_DIR
from selenium.webdriver.common.by import By


class BasePage:

    def __init__(self, driver: WebElement):
        self.driver = driver

    def wait_eleVisible(self, loc, timeout=30, poll_frequency=0.2, mark=None):
        """
        :param loc:元素定位表达;元组类型,表达方式(元素定位类型,元素定位方法)
        :param timeout:等待的上限
        :param poll_frequency:轮询频率
        :param mark:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return:None
        """
        logger.info('{} 等待元素可见:{}'.format(mark, loc))
        try:
            start = time.time()
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.visibility_of_element_located(loc))
            end = time.time()
            logger.info('等待时长:%.2f 秒' % (end - start))
            return True
        except:
            logger.exception('{} 等待元素可见失败:{}'.format(mark, loc))
            # 截图
            self.save_webImgs(mark)
            # raise NoSuchElementException
            return False

    # 查找一个元素element
    def find_Element(self, loc, mark=None) -> WebElement:
        logger.info('{} 查找元素 {}'.format(mark, loc))
        try:
            return self.driver.find_element(*loc)
        except:
            logger.exception('查找元素失败.')
            # 截图
            self.save_webImgs(mark)
            raise

    # 查找元素elements
    def find_Elements(self, loc, mark=None) -> List[WebElement]:
        logger.info('{} 查找元素 {}'.format(mark, loc))
        try:
            logger.info(f'type == {type(self.driver.find_elements(*loc))}, eles == {self.driver.find_elements(*loc)}')
            return self.driver.find_elements(*loc)
        except:
            logger.exception('查找元素失败.')
            # 截图
            self.save_webImgs(mark)
            raise

    # 输入操作
    def input_Text(self, loc, text, mark=None):
        # 查找元素
        ele = self.find_Element(loc, mark)
        # 输入操作
        logger.info('{} 在元素 {} 中输入文本: {}'.format(mark, loc, text))
        try:
            ele.send_keys(text)
        except:
            logger.exception('输入操作失败')
            # 截图
            self.save_webImgs(mark)
            raise

    # 清除操作
    def clean_Input_Text(self, loc, mark=None):
        ele = self.find_Element(loc, mark)
        # 清除操作
        logger.info('{} 在元素 {} 中清除'.format(mark, loc))
        try:
            ele.clear()
            ele.send_keys('')
        except:
            logger.exception('清除操作失败')
            # 截图
            self.save_webImgs(mark)
            raise

    # 点击操作
    def click_Element(self, loc, mark=None):
        # 先查找元素在点击
        ele = self.find_Element(loc, mark)
        # 点击操作
        logger.info('{} 在元素 {} 中点击'.format(mark, loc))
        try:
            ele.click()
        except:
            logger.exception('点击操作失败')
            # 截图
            self.save_webImgs(mark)
            raise

    # 获取文本内容
    def get_Text(self, loc, mark=None):
        # 先查找元素再获取文本内容
        ele = self.find_Element(loc, mark)
        # 获取文本
        logger.info('{} 在元素 {} 中获取文本'.format(mark, loc))
        try:
            text = ele.text
            logger.info('{} 元素 {} 的文本内容为 {}'.format(mark, loc, text))
            return text
        except:
            logger.exception('获取元素 {} 的文本内容失败,报错信息如下:'.format(loc))
            # 截图
            self.save_webImgs(mark)
            raise

    # 获取属性值
    def get_Element_Attribute(self, loc, mark=None):
        # 先查找元素再去获取属性值
        ele = self.find_Element(loc, mark)
        # 获取元素属性值
        logger.info('{} 在元素 {} 中获取属性值'.format(mark, loc))
        try:
            ele_attribute = ele.get_attribute()
            logger.info('{} 元素 {} 的文本内容为 {}'.format(mark, loc, ele_attribute))
            return ele_attribute
        except:
            logger.exception('获取元素 {} 的属性值失败,报错信息如下:'.format(loc))
            self.save_webImgs(mark)
            raise

    # iframe 切换
    def switch_iframe(self, frame_refer, timeout=20, poll_frequency=0.5, mark=None):
        # 等待 iframe 存在
        logger.info('iframe 切换操作:')
        try:
            # 切换 == index\name\id\WebElement
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.frame_to_be_available_and_switch_to_it(frame_refer))
            time.sleep(0.5)
            logger.info('切换成功')
        except:
            logger.exception('iframe 切换失败!')
            # 截图
            self.save_webImgs(mark)
            raise

    # 窗口切换：new - 切换到新窗口，default - 回到默认的窗口
    def switch_window(self, name, cur_handles=None, timeout=20, poll_frequency=0.5, mark=None):
        """
        调用之前要获取window_handles
        :param name: new 代表最新打开的一个窗口. default 代表第一个窗口. 其他的值表示为窗口的 handles
        :param cur_handles:
        :param timeout:等待的上限
        :param poll_frequency:轮询频率
        :param mark:等待失败时,截图操作,图片文件中需要表达的功能标注
        :return:
        """
        try:
            if name == 'new':
                if cur_handles is not None:
                    logger.info('切换到最新打开的窗口')
                    WebDriverWait(self.driver, timeout, poll_frequency).until(EC.new_window_is_opened(cur_handles))
                    window_handles = self.driver.window_handles
                    self.driver.swich_to.window(window_handles[-1])
                else:
                    logger.exception('切换失败,没有要切换窗口的信息!')
                    self.save_webImgs(mark)
                    # raise
            elif name == 'default':
                logger.info('切换到默认页面')
                self.driver.switch_to.default()
            else:
                logger.info('切换到为 handles 的窗口')
                self.driver.swich_to.window(name)
        except:
            logger.exception('切换窗口失败!')
            # 截图
            self.save_webImgs(mark)
            raise

    # 截图
    def save_webImgs(self, mark=None):
        # filepath = 指图片保存目录/mark(页面功能名称)_当前时间到秒.png
        # 当前时间
        dateNow = str(datetime.datetime.now()).split('.')[0]
        # 路径
        filePath = '{}/{}_{}.png'.format(IMAGE_DIR, mark, dateNow)
        try:
            self.driver.save_screenshot(filePath)
            logger.info('截屏成功,图片路径为{}'.format(filePath))
        except:
            logger.exception('截屏失败!')

    # 点击文本元素
    def click_Text(self, text, mark=None):

        elem = (By.XPATH, f'//*[text()="{text}"]')
        try:
            logger.info(f'{mark} 在元素 {elem} 中点击')
            time.sleep(1)
            self.find_Element(elem).click()
        except:
            logger.exception('点击文本失败！')
            self.save_webImgs(mark)

    # 清楚输入框的文本（当clear无法使用时，使用）
    def clean_Text(self, el):
        from selenium.webdriver.common.keys import Keys
        ele = self.find_Element(el)
        ele.send_keys(Keys.CONTROL + 'a')  # CTRL + a ：全选
        ele.send_keys(Keys.DELETE)  # 删除

    def is_Enabled(self, el, mark=None):
        """
        检查元素是否可用、可点击
        """
        logger.info(f'{mark} 在元素 {el} 中检查是否可点击、可用')
        return self.find_Element(el).is_enabled()

    def check_text(self, text):
        from selenium.webdriver.common.by import By
        x = (By.XPATH, f'//*[text()="{text}"]')
        try:
            if self.wait_eleVisible(x):
                logger.info(f'找到toast提示语：{text}')
                return True
        except NoSuchElementException:
            logger.exception(f'找不到该{text}toast提示，请检查文件以及标点符号！')
            return False

    def upload_file(self, loc, filepath):
        import os
        try:
            self.click_Element(loc, mark='上传')
            path = os.path.abspath('..') + '\\uploadjson.exe'  # 上传文件
            os.system(fr'{path} {filepath}')
            time.sleep(2)
        except:
            raise

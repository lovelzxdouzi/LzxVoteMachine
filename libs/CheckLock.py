from libs.Login import *

class CheckLock(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, 0.5)  # 等待时间
        self.driver.set_window_size(1000, 820)
        """
        # 读取日志
        """
        self.logger = logging.getLogger('test')

    def to_page(self, url):
        self.driver.get(url)

    def run(self):
        # 跳转去安全中心页面
        self.to_page(security_url)
        self.driver.implicitly_wait(0.1)

        try:
            strange_message = self.wait.until(EC.presence_of_element_located((By.XPATH, account_strange_message_path)))
            self.driver.implicitly_wait(0.1)
            strange_text = strange_message.text
            # 账号被锁定
            self.logger.debug('账号被锁定，切号，页面信息：%s', strange_text)
            print('账号被锁定，切号，页面信息：%s' %(strange_text))
            config.setIsLock(True)
        except TimeoutException as e:
            self.logger.debug('账号没被锁定')
        except ElementNotVisibleException as w:
            self.logger.debug('账号没被锁定')

        return self.driver

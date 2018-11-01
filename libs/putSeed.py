from libs.Login import *
from libs.doComment import *


class putSeed(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.set_window_size(600, 920)
        """
        # 读取日志
        """
        self.logger = logging.getLogger('test')

    def to_page(self, url):
        self.driver.get(url)
        time.sleep(5)

    def run(self):
        self.logger.debug('开始种土豆')
        # 进入挖土豆超话页
        self.to_page(wtd_url)
        self.driver.implicitly_wait(0.1)

        try:
            # 点击 textarea
            seed_textarea = self.wait.until(EC.presence_of_element_located((By.XPATH, seed_textarea_path)))
            self.driver.implicitly_wait(0.1)
            seed_textarea.click()
            self.driver.implicitly_wait(0.1)
            seed_textarea.clear()
            self.driver.implicitly_wait(0.1)

            # 填写内容：
            # 随机生成评论字符串
            text = seed_context[random.randint(0, 5)]
            seed_textarea.send_keys(text)
            self.driver.implicitly_wait(0.1)

            # 确认并发送
            seed_send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, seed_send_btn_path)))
            self.driver.implicitly_wait(0.1)
            seed_send_btn.click()
            self.driver.implicitly_wait(0.1)

            self.driver.refresh()
            self.driver.implicitly_wait(0.1)
        except TimeoutException as t:
            self.logger.debug('出现超时现象 - %s', t)
            return self.run()

        return self.driver

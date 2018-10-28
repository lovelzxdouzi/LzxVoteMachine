from libs.Login import *
from libs.path_url_lib import *

import logging

class AutoSign(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30, 0.5)  # 等待时间
        self.driver.set_window_size(1000, 820)
        """
        # 读取日志
        """
        self.logger = logging.getLogger('test')

    def to_page(self, url):
        self.driver.get(url)

    def doQuery(self):
        self.logger.debug('Do Query')
        self.logger.debug('检查title路径')
        title = self.wait.until(EC.presence_of_element_located((By.XPATH, title_path)))
        self.logger.debug('检查title路径：成功')
        self.logger.debug('检查focus button路径')
        focus_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, focus_btn_path)))
        self.logger.debug('检查focus button路径：成功')
        info = focus_btn.text
        self.logger.debug('focus button info: %s', info)
        
        time.sleep(5)
        # 如果是已关注，则点击右边的签到按钮:
        if info == 'Y 已关注g':
            sign_btn = self.driver.find_element_by_xpath(sign_btn_poth)

            if sign_btn.text != '已关注':
                sign_btn.click()
                print('INFO: [{}] 签到完成....'.format(title.text))
            elif sign_btn.text == '已签到':
                pass

        # 如果还未关注，则点击关注，再签到
        elif info == '+关注':
            focus_btn.click()
            time.sleep(5)
            try:
                sign_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, sign_btn_poth)))
                sign_btn.click()
            except TimeoutException as e:
                print(e)
                self.driver.refresh()
                sign_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, sign_btn_poth)))
                sign_btn.click()
            except ElementNotVisibleException as w:
                print(w)
                self.driver.refresh()
                sign_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, sign_btn_poth)))
                sign_btn.click()
                print('INFO: [{}] 签到完成....'.format(title.text))
            time.sleep(3)

    def run(self):
        url_set = [wtd_url, zdz_url, cdb_url, xkl_url]
        self.doQuery()
        for url in url_set:
            self.to_page(url)
            self.doQuery()

        return self.driver

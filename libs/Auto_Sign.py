from libs.Login import *

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

    def doQuery(self, url):
        # self.logger.debug('Do Query')
        # self.logger.debug('检查title路径')
        self.to_page(url)

        title = self.wait.until(EC.presence_of_element_located((By.XPATH, title_path)))
        self.driver.implicitly_wait(0.1)
        # self.logger.debug('检查title路径：成功')
        # self.logger.debug('检查focus button路径')
        focus_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, focus_btn_path)))
        self.driver.implicitly_wait(0.1)
        # self.logger.debug('检查focus button路径：成功')
        info = focus_btn.text
        self.logger.debug('focus button info: %s', info)
        
        time.sleep(5)
        self.driver.implicitly_wait(0.1)
        # 如果是已关注，则点击右边的签到按钮:
        if info == 'Y 已关注g':
            try:
                sign_btn = self.driver.find_element_by_xpath(sign_btn_poth)
                if sign_btn.text != '已关注':
                    sign_btn.click()
                    self.driver.implicitly_wait(0.1)
                    self.logger.debug('%s 签到完成....', title.text)
                    print('INFO: [{}] 签到完成....'.format(title.text))
                elif sign_btn.text == '已签到':
                    pass
            except NoSuchElementException:
                self.logger.debug('没有找到签到按钮,准备刷新一下...')
                print(u'没有找到签到按钮,准备刷新一下...')
                self.driver.refresh()
                self.driver.implicitly_wait(0.1)
                self.doQuery(url)

        # 如果还未关注，则点击关注，再签到
        elif info == '+关注':
            focus_btn.click()
            self.driver.implicitly_wait(0.1)
            time.sleep(5)
            
            try:
                sign_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, sign_btn_poth)))
                self.driver.implicitly_wait(0.1)
                sign_btn.click()
                self.driver.implicitly_wait(0.1)
                print('INFO: [{}] 签到完成....'.format(title.text))
            except TimeoutException as e:
                print(e)
                self.logger.debug('关注失败，超时：%s', e)
            except ElementNotVisibleException as w:
                print(w)
                self.logger.debug('关注失败，没有关注按钮：%s', w)

            time.sleep(3)
            self.driver.implicitly_wait(0.1)

    def run(self):
        url_set = [mainst_url, wtd_url, zdz_url, cdb_url, xkl_url]

        for url in url_set:
            try:
                self.doQuery(url)
            # 在这里except WebDriverWait会出现问题，所以暂时先注释
            # except WebDriverWait as w:
            except Exception as w:
                self.logger.debug('WebDriverWait - 出现问题')
                self.logger.debug('WebDriverWait - %s', w)
                print(w)
                continue

        return self.driver

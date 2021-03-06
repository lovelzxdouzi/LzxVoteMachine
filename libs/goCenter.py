from libs.path_url_lib import *
from libs.Login import *

import logging

class goCenter(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.set_window_size(500, 980)
        """
        # 读取日志
        """
        self.logger = logging.getLogger('test')

    def to_page(self, url):
        self.driver.get(url)
        time.sleep(5)

    def run(self):
        # 1. 进任务中心领分
        self.logger.debug('进任务中心领分')

        global module
        self.driver.set_window_size(300, 980)
        # 先进送分页面，如果没分，送分按钮就是去任务中心的按钮
        self.to_page(vote_url)
        try:
            center = self.wait.until(EC.presence_of_element_located((By.XPATH, center_path)))
        except TimeoutException:
            self.logger.debug('现在已经没积分啦!准备进入任务中心领分...')
            print(u'现在已经没积分啦!准备进入任务中心领分...')
            center = self.driver.find_element_by_xpath(vote_btn_path)
        center.click()
        time.sleep(5)

        self.logger.debug('任务中心：判断老号还是新号')
        # 判断老号还是新号，看 任务中心的 dl 是 2个还是 3个
        try:
            first_title = self.wait.until(EC.presence_of_element_located((By.XPATH, first_title_path))).text
        except WebDriverException as e:
            self.logger.debug('没有找到任务中心的第一个标题，可能不是任务中心，重新进入任务中心。')
            return self.run()

        self.logger.debug('第一个标题是：%s', first_title)
        
        moudle = 2
        if first_title == '新手任务':
            # 是新号：
            try:
                new_user_bonus = self.driver.find_element_by_xpath(new_user_bonus_path)
                text = new_user_bonus.text
                if text == '去关注' or text == '已领取' or text == '打开' or text == '下载':
                    pass
                else:
                    new_user_bonus.click()
                    time.sleep(1)
            except NoSuchElementException:
                print(u'新手关注超话任务已完成...')
                pass
            except WebDriverException as e:
                print(e.stacktrace)
                pass
        elif first_title == '每日任务':
            # 相对而言是老号：
            moudle = 1
        

        """
        self.logger.debug('读取lxfw分: %s', first_title)
        if first_title == '每日任务':
            # 是二手号
            self.logger.debug('二手号')
            try:
                lxfw_bonus = self.driver.find_element_by_xpath(old_lxfw_bonus_path)
            except WebDriverException as e:
                self.driver.refresh()
                lxfw_bonus = self.driver.find_element_by_xpath(old_lxfw_bonus_path)
        else:
            self.logger.debug('其他号')
            try:
                lxfw_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, lxfw_bonus_path)))
            except WebDriverException as e:
                self.driver.refresh()
                lxfw_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, lxfw_bonus_path)))
        """
            

        #不用在任务中心点击评论按钮
        """
        self.logger.debug('读取comment分')
        comment_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, comment_bonus_path)))
        """

        # 获取连续访问按键，如果有分就领取
        self.logger.debug('任务中心：获取连续访问按键')
        try:
            lxfw_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, lxfw_bonus_path.format(moudle))))
            if lxfw_bonus.text == '已领取':
                pass
            else:
                lxfw_bonus.click()
                time.sleep(2)
        except WebDriverException as e:
            self.logger.debug('WebDriverException - 获取连续访问案件出错，跳过')
            self.logger.debug('WebDriverException - %s', e)

        # 不用在任务中心点击20条被评论按钮
        """
        self.logger.debug('Scroll into View')
        self.driver.execute_script("arguments[0].scrollIntoView();", comment_bonus)
        time.sleep(2)

        self.logger.debug('读取20评论分')
        twenty_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, twenty_bonus_path)))
        if twenty_bonus.text == '':
            twenty_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, saved_twenty_bonus_path)))
        if twenty_bonus.text == '去完成' or twenty_bonus.text == '已完成':
            pass
        else:
            twenty_bonus.click()
        """

        return self.driver

    def sendScore(self):
        # 2. 送分
        self.to_page(vote_url)
        self.driver.implicitly_wait(0.1)

        try:
            score_info = self.wait.until(EC.presence_of_element_located((By.XPATH, score_info_path)))
            self.driver.implicitly_wait(0.1)

            points = 0
            if eval(re.sub('\D', '', score_info.text)) == 0:
                return print('现在已经没有积分啦！')
            else:
                print(score_info.text)
                points += eval(re.sub('\D', '', score_info.text))

            select_all_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, select_all_btn_path)))
            self.driver.implicitly_wait(0.1)
            select_all_btn.click()
            self.driver.implicitly_wait(0.1)
            time.sleep(2)

            vote_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, vote_btn_path)))
            self.driver.implicitly_wait(0.1)
            vote_btn.click()
            self.driver.implicitly_wait(0.1)
            print('送分成功！')
            config.addScore(points)
            time.sleep(3)

            rank_info = self.wait.until(EC.presence_of_element_located((By.XPATH, rank_info_path)))
            self.driver.implicitly_wait(0.1)
            desc_info = self.wait.until(EC.presence_of_element_located((By.XPATH, desc_info_path)))
            self.driver.implicitly_wait(0.1)
            print(rank_info.text, ',', desc_info.text)
        except TimeoutException as t:
            self.logger.debug('出现超时现象 - %s', t)
            return self.sendScore()

        return self.driver

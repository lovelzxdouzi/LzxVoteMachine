from libs.path_url_lib import *
from libs.Login import *


class goCenter(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.set_window_size(500, 980)

    def to_page(self, url):
        self.driver.get(url)
        time.sleep(5)

    def run(self):
        # 1. 进任务中心领分
        self.to_page(vote_url)
        try:
            center = self.wait.until(EC.presence_of_element_located((By.XPATH, center_path)))
        except TimeoutException:
            print(u'现在已经没积分啦!')
            center = self.driver.find_element_by_xpath(vote_btn_path)
        center.click()
        time.sleep(5)

        try:
            new_user_bonus = self.driver.find_element_by_xpath(new_user_bonus_path)
            if new_user_bonus.text == '已领取' or new_user_bonus.text == '打开':
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

        lxfw_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, lxfw_bonus_path)))
        comment_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, comment_bonus_path)))

        if lxfw_bonus.text == '已领取':
            pass
        else:
            lxfw_bonus.click()
            time.sleep(2)

        self.driver.execute_script("arguments[0].scrollIntoView();", comment_bonus)
        time.sleep(2)

        twenty_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, twenty_bonus_path)))
        if twenty_bonus.text == '':
            twenty_bonus = self.wait.until(EC.presence_of_element_located((By.XPATH, saved_twenty_bonus_path)))
        if twenty_bonus.text == '去完成' or twenty_bonus.text == '已完成':
            pass
        else:
            twenty_bonus.click()

        return self.driver

    def sendScore(self):
        # 2. 送分
        self.to_page(vote_url)
        score_info = self.wait.until(EC.presence_of_element_located((By.XPATH, score_info_path)))

        if eval(re.sub('\D', '', score_info.text)) == 0:
            return print('现在已经没有积分啦！')
        else:
            print(score_info.text)

        select_all_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, select_all_btn_path)))
        select_all_btn.click()
        time.sleep(2)

        vote_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, vote_btn_path)))
        vote_btn.click()
        print('送分成功！')
        time.sleep(3)

        rank_info = self.wait.until(EC.presence_of_element_located((By.XPATH, rank_info_path)))
        desc_info = self.wait.until(EC.presence_of_element_located((By.XPATH, desc_info_path)))
        print(rank_info.text, ',', desc_info.text)

        return self.driver


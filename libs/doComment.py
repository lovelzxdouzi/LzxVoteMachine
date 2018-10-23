from libs.Login import *
from libs.contextLib import *
from libs.path_url_lib import *


class doComments(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        self.driver.set_window_size(640, 950)

    def to_page(self):
        self.driver.get(wtd_url)

    def run(self):
        # 循环 8 次评论过程
        self.to_page()
        self.driver.refresh()

        head = self.wait.until(EC.presence_of_element_located((By.XPATH, head_path)))
        self.driver.execute_script("arguments[0].scrollIntoView();", head)
        time.sleep(2)

        # 进入 帖子tab

        for cursor in range(1, 9):
            # 每次重新进入到 帖子tab 页面，都选取第一个帖子观察
            info_num = self.wait.until(EC.presence_of_element_located((By.XPATH, count_path.format(cursor)))).text
            if info_num == '评论':
                count = 0
            else:
                count = eval(info_num)

            # 若 大于19 则视为已经满了，则向下遍历 wrapper，找到一个满足条件的
            while count > 19:
                cursor += 1
                count = self.wait.until(EC.presence_of_element_located((By.XPATH, count_path.format(cursor))))
                self.driver.execute_script("arguments[0].scrollIntoView();", count)
                time.sleep(1)
                count = eval(count.text)

            # 检查 wrapper 的评论数量，小于等于19 则 给评论

            print('caught count: ', count)
            # 点击评论按钮
            comment_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, comment_btn_path.format(cursor))))
            try:
                comment_btn.click()
            except WebDriverException as e:
                print(e)
                count -= 1
                continue

            time.sleep(5)

            # 填写评论内容
            textarea = self.wait.until(EC.presence_of_element_located((By.XPATH, textarea_path.format(cursor))))
            textarea.click()
            textarea.clear()

            # 随机生成评论字符串
            text = context[random.randint(0, 36)]
            textarea.send_keys('v'+text)

            # 发送评论
            send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, send_btn_path.format(cursor))))
            send_btn.click()

            # 等待 '发送完成' 提示消失
            print('第{}次评论完成 ...'.format(cursor))
            time.sleep(2)
            try:
                comment_btn.click()
            except WebDriverException as e:
                print(e)
                cursor += 1
                continue

            self.driver.execute_script("arguments[0].scrollIntoView();", comment_btn)
            time.sleep(5 + random.randint(0, 10))

        return self.driver

from libs.Login import *

class doComments(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 30, 0.5)
        self.driver.set_window_size(640, 950)
        """
        # 读取日志
        """
        self.logger = logging.getLogger('test')

    def to_page(self):
        self.driver.get(wtd_url)

    def run(self):
        self.logger.debug('开始挖土豆')
        
        # 跳转去挖土豆超话
        self.to_page()
        self.driver.implicitly_wait(0.1)
        self.driver.refresh()
        self.driver.implicitly_wait(0.1)

        # 移动到超话head部分
        try:
            head = self.wait.until(EC.presence_of_element_located((By.XPATH, head_path)))
            self.driver.implicitly_wait(0.1)
            self.driver.execute_script("arguments[0].scrollIntoView();", head)
        except TimeoutException as t:
            # 如果读取head部分失败，可能跳转没有成功, 重新跳转
            self.logger.debug('移动到超话head部分出现超时错误：%s', t)
            return self.run()

        time.sleep(1)
        self.driver.implicitly_wait(0.1)

        # 循环 8 次评论过程
        # 进入 帖子tab
        rec = 1
        for cursor in range(1, 9):
            try:
                # 每次重新进入到 帖子tab 页面，都选取第一个帖子观察
                info_num = self.wait.until(EC.presence_of_element_located((By.XPATH, count_path.format(cursor))))
                self.driver.implicitly_wait(0.1)
                if info_num.text == '评论':
                    count = 0
                else:
                    count = eval(info_num.text)

                # 若 大于19 则视为已经满了，则向下遍历 wrapper，找到一个满足条件的
                while count > 19:
                    info_num = self.wait.until(EC.presence_of_element_located((By.XPATH, count_path.format(cursor))))
                    self.driver.implicitly_wait(0.1)
                    self.driver.execute_script("arguments[0].scrollIntoView();", info_num)
                    self.driver.implicitly_wait(0.1)
                    cursor += 1
                    time.sleep(1)
                    self.driver.implicitly_wait(0.1)
                    if info_num.text == '评论':
                        count = 0
                    else:
                        count = eval(info_num.text)

                # 检查 wrapper 的评论数量，小于等于19 则 给评论

                self.logger.debug('当前帖子评论数:%d', count)
                print('INFO: 当前帖子评论数: ', count)
                # 点击评论按钮
                comment_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, comment_btn_path.format(cursor))))
                self.driver.implicitly_wait(0.1)
                
                comment_btn.click()

                time.sleep(3)
                self.driver.implicitly_wait(0.1)

                # 填写评论内容
                textarea = self.wait.until(EC.presence_of_element_located((By.XPATH, textarea_path.format(cursor))))
                self.driver.implicitly_wait(0.1)
                
                textarea.click()
                self.driver.implicitly_wait(0.1)
                textarea.clear()

                # 随机生成评论字符串
                text = context[random.randint(0, 15)]
                textarea.send_keys(text)
                self.driver.implicitly_wait(0.1)

                # 发送评论
                send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, send_btn_path.format(cursor))))
                self.driver.implicitly_wait(0.1)
                send_btn.click()
                self.driver.implicitly_wait(0.1)

                # 等待 '发送完成' 提示消失
                self.logger.debug('第%d次评论完成 ...', count)
                print('第{}次评论完成 ...'.format(rec))
                rec += 1
                time.sleep(1)
                self.driver.implicitly_wait(0.1)
            except TimeoutException as t:
                print(t)
                continue
            except WebDriverException as e:
                print(e)
                continue

            # 再次点击 评论数字 收起评论条目
            try:
                comment_btn.click()
                self.driver.implicitly_wait(0.1)
            except WebDriverException as e:
                print(e)
                self.driver.execute_script("arguments[0].scrollIntoView();", comment_btn)
                self.driver.implicitly_wait(0.1)
                continue

            self.driver.implicitly_wait(0.1)
            # 这个 scroll 就是  ‘过’ 当前这个帖子块
            self.driver.execute_script("arguments[0].scrollIntoView();", comment_btn)
            time.sleep(3 + random.randint(0, 3))
            self.driver.implicitly_wait(0.1)

        return self.driver


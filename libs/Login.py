# -*- coding: utf-8 -*-
from selenium import webdriver

# 导入期望类
from selenium.webdriver.support import expected_conditions as EC

# 导入By类
from selenium.webdriver.common.by import By

# 导入显式等待类
from selenium.webdriver.support.ui import WebDriverWait

# 导入异常类
from selenium.common.exceptions import *

from libs.Compare import *
from selenium.webdriver import ActionChains
from libs.path_url_lib import *
from io import BytesIO
import time
import re
from os import listdir

import logging

TEMPLATES_FOLDER = "./image/"


class Login(object):

    def __init__(self, driver, username, password):
        self.url = "https://passport.weibo.cn/signin/login"  # 移动版微博登录页
        self.driver = driver  # 获得 selenium driver
        self.wait = WebDriverWait(self.driver, 10, 0.5)  # 等待时间
        self.username = username
        self.password = password
        """
        # 读取日志
        """
        self.logger = logging.getLogger('test')

    def to_page(self, url):
        self.driver.get(url)
        time.sleep(3)

    def open(self):
        """
        打开网页输入账号密码，并点击
        :return:
        """
        # 进入移动端微博登录页面
        self.logger.debug('进入移动端微博登录页面')
        
        self.driver.set_window_size(100, 455)
        self.driver.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, "loginName")))
        password = self.wait.until(
            EC.presence_of_element_located((By.ID, "loginPassword"))
        )
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "loginAction")))

        # 填入账号密码
        self.logger.debug('填入账号密码')
        
        username.clear()
        username.send_keys(self.username)
        password.send_keys(self.password)
        button.click()

        # 等待 验证轨迹图片 的第一次导引动画
        self.logger.debug('等待 验证轨迹图片 的第一次导引动画')
        
        time.sleep(4)
        self.errCheck()

    def errCheck(self):
        errmsg = self.wait.until(EC.element_to_be_clickable((By.ID, "errorMsg"))).text
        if len(errmsg) > 10:
            self.logger.debug('出现红字errMsg, 需要刷新, 重新获取轨迹图...')
            print(u'INFO: 出现红字errMsg, 需要刷新, 重新获取轨迹图...')
            self.driver.refresh()
            self.open()
        else:
            self.logger.debug('没有出现登录errMsg.')
            print(u'INFO: 没有出现登录errMsg.')

    def get_position(self):
        """
        获取验证码位置
        :return:
        """
        self.logger.debug('获取验证码位置')
        
        # 获取轨迹验证码图片
        try:
            img = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "patt-holder-body"))
            )

            # 获得图片准确位置
            location = img.location
            size = img.size
            top, bottom, left, right = (
                location["y"],
                location["y"] + size["height"],
                location["x"],
                location["x"] + size["width"],
            )

            return top, bottom, left, right
        except TimeoutException as e:
            self.logger.debug('TimeoutException - %s', e)
            print(e.args)
            self.open()
        except NoSuchElementException as e:
            self.logger.debug('NoSuchElementException - %s', e)
            print(e.args)
            self.open()
        time.sleep(2)

    def get_image(self, name="captcha.png"):
        """
        获取验证码图片
        :param name: 验证码图片名字
        :return:
        """
        self.logger.debug('获取验证码图片')
        
        top, bottom, left, right = self.get_position()
        # 获取整个网页截图
        screenshot = self.driver.get_screenshot_as_png()
        # 将截图读到内存
        screenshot = Image.open(BytesIO(screenshot))
        screenshot.save('src.png')
        # 截取验证码图片
        captcha = screenshot.crop((left, top, right, bottom))
        # screenshot.show()  # 展示原始截图图片
        captcha.save(name)
        # captcha.show()
        return captcha

    # def get_many_image(self):
    #     '''
    #     批量获取验证码
    #     :return:
    #     '''
    #     count = 0
    #     for i in range(100):
    #         self.open()
    #         self.get_image(str(count)+'.png')
    #         count += 1

    def compare(self, dic, image_dir, template_name):
        """
        识别相似验证码
        :param image:待识别验证码
        :param template: 模板
        :return: True or Flase
        """
        # 相似度阈值
        threshold = 0.96
        compare_image = CompareImage()
        result = compare_image.compare_image(image_dir, template_name)
        template_name = re.sub(TEMPLATES_FOLDER, '', template_name)
        dic[template_name] = result

    def detect_image(self, image):
        """
        匹配图片
        :param image: 图片
        :return: 拖动顺序
        """
        self.logger.debug('匹配图片')
        
        dic = {}  # 相似度记录字典
        for template_name in listdir(TEMPLATES_FOLDER):
            pic_name = template_name
            template_name = TEMPLATES_FOLDER + template_name
            self.compare(dic, './captcha.png', template_name)

        # 返回顺序
        pic_name = max(dic, key=dic.get)
        numbers = [int(number) for number in list(pic_name.split(".")[0])]
        print("INFO: 拖动顺序", numbers)
        return numbers

    def move(self, numbers):
        """
        根据顺序拖动
        :param numbers:
        :return:
        """
        self.logger.debug('根据顺序拖动')
        
        # 获得四个按点
        circles = self.driver.find_elements_by_css_selector(".patt-wrap .patt-circ")
        dx = dy = 0
        for index in range(4):
            # 获取相对应的按点
            circle = circles[numbers[index] - 1]
            # 如果是第一个按点
            if index == 0:
                # 点击不放
                ActionChains(self.driver).move_to_element_with_offset(
                    circle, circle.size["width"] / 2, circle.size["height"] / 2
                ).click_and_hold().perform()
            else:
                # 小幅移动次数
                times = 25
                for i in range(times):
                    ActionChains(self.driver).move_by_offset(
                        dx / times, dy / times
                    ).perform()
                    time.sleep(1 / times)
            # 如果这是最后一次循环
            if index == 3:
                # 松开鼠标
                ActionChains(self.driver).release().perform()
            else:
                # 计算下一次偏移
                dx = (
                        circles[numbers[index + 1] - 1].location["x"] - circle.location["x"]
                )
                dy = (
                        circles[numbers[index + 1] - 1].location["y"] - circle.location["y"]
                )

        move_ret = self.driver.find_element_by_xpath(move_ret_path)
        if move_ret == '验证码已过期' or move_ret == '验证失败':
            return True
        else:
            return False

    def loginCheck(self):
        # 登录检查，是否真的登录了账号:
        self.driver.set_window_size(900, 455)
        self.to_page(mainst_url)

        print(u'INFO: 登录检查...')
        self.logger.debug('登录检查...')

        # 检查是不是完善资料页面
        is_detail_page = True
        try:
            self.logger.debug('检查是否是完善资料页面')
            fill_in_details = self.wait.until(EC.presence_of_element_located((By.XPATH, fill_in_details_path)))
        except TimeoutException as t:
            is_detail_page = None

        if is_detail_page:
            self.logger.debug('是完善资料页面，跳过')
        else:
            self.logger.debug('不是完善资料页面，进行下一步检查')

        # 检查登陆
        gn_position = self.wait.until(EC.presence_of_element_located((By.XPATH, gn_position_path)))

        html = gn_position.get_attribute('innerHTML')

        if '注册' in html or '登录' in html:
            self.logger.debug('登录异常，重新登录中...')
            print(u'INFO: 登录异常，重新登录中...')
            self.run()
        else:
            self.logger.debug('登录检查通过...')
            print(u'INFO: 登录检查通过...')

    def run(self):
        """
        主函数
        :return: driver 返回浏览器driver 以备之后使用
        """
        self.open()
        loop = True
        # 预防 拖动轨迹 失败
        while loop:
            image = self.get_image()
            numbers = self.detect_image(image)
            loop = self.move(numbers)
            time.sleep(5)
        self.loginCheck()

        return self.driver

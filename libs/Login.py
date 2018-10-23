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
from io import BytesIO
import time
import re
from os import listdir

TEMPLATES_FOLDER = "./image/"


class Login(object):

    def __init__(self,driver, username, password):
        self.url = "https://passport.weibo.cn/signin/login"  # 移动版微博登录页
        self.driver = driver  # 获得 selenium driver
        self.driver.set_window_size(100, 455)
        self.wait = WebDriverWait(self.driver, 10, 0.5)  # 等待时间
        self.username = username
        self.password = password

    def open(self):
        """
        打开网页输入账号密码，并点击
        :return:
        """
        # 进入移动端微博登录页面
        self.driver.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, "loginName")))
        password = self.wait.until(
            EC.presence_of_element_located((By.ID, "loginPassword"))
        )
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "loginAction")))

        # 填入账号密码
        username.clear()
        username.send_keys(self.username)
        password.send_keys(self.password)
        button.click()
        time.sleep(5)

    def get_position(self):
        """
        获取验证码位置
        :return:
        """

        # 获取轨迹验证码图片
        try:
            img = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "patt-holder-body"))
            )
        except TimeoutException as e:
            print(e.args)
            self.open()
        except NoSuchElementException as e:
            print(e.args)
            self.open()
        time.sleep(2)

        # 获得图片准确位置
        location = img.location
        print('location:', location)
        size = img.size
        print('size:', size)
        top, bottom, left, right = (
            location["y"],
            location["y"] + size["height"],
            location["x"],
            location["x"] + size["width"],
        )

        return top, bottom, left, right

    def get_image(self, name="captcha.png"):
        """
        获取验证码图片
        :param name: 验证码图片名字
        :return:
        """
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
        dic = {}  # 相似度记录字典
        for template_name in listdir(TEMPLATES_FOLDER):
            pic_name = template_name
            template_name = TEMPLATES_FOLDER + template_name
            self.compare(dic, './captcha.png', template_name)

        # 返回顺序
        pic_name = max(dic, key=dic.get)
        numbers = [int(number) for number in list(pic_name.split(".")[0])]
        print("拖动顺序", numbers)
        return numbers

    def move(self, numbers):
        """
        根据顺序拖动
        :param numbers:
        :return:
        """
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
                times = 30
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
        time.sleep(2)

    def run(self):
        """
        主函数
        :return: driver 返回浏览器driver 以备之后使用
        """
        self.open()
        image = self.get_image()
        numbers = self.detect_image(image)
        self.move(numbers)
        time.sleep(15)

        return self.driver
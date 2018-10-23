from libs.Login import *


class Status(object):
    def __init__(self):
        self.status = 0

    def _Login(self):
        # 登录结束
        self.status = 20

    def _AutoSign(self):
        # 自动签到结束
        self.status = 40

    def _getScore(self):
        self.status = 60

    def _comment_over(self):
        self.status = 80

    def _putSeed(self):
        self.status = 90

    def _sendScore(self):
        self.status = 100

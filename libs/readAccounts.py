from libs.Login import *
from libs.path_url_lib import *
import os


class readAccounts(object):
    def __init__(self):
        account_set = open('./account_set.txt')
        all_lines = account_set.readlines()

        self.accounts = {}

        for line in all_lines:
            line = re.sub('\n', '', line)
            if line == '':
                continue
            account = line.split('----')[0]
            password = line.split('----')[1]
            

            self.accounts[account] = password

    def get(self):
        return self.accounts


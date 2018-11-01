class Configuration(object):
    def __init__(self):
        self.go_for_next_account = False
        self.is_lock = False
        self.success = 0
        self.error = 0
        self.lock = 0
        self.score = 0

    def reset(self):
        self.go_for_next_account = False
        self.is_lock = False

    def setNextAccount(self, flag):
        self.go_for_next_account = flag

    def getNextAccount(self):
        return self.go_for_next_account

    def setIsLock(self, flag):
        self.is_lock = flag

    def getIsLock(self):
        return self.is_lock

    def addSuccess(self):
        self.success += 1

    def addError(self):
        self.error += 1

    def addLock(self):
        self.lock += 1

    def addScore(self, points):
        self.score += points

    def getSuccess(self):
        return self.success

    def getError(self):
        return self.error

    def getLock(self):
        return self.lock

    def getScore(self):
        return self.score

config = Configuration()    


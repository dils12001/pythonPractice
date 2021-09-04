

class User(object):
    def __init__(self,userId,passwd,name,identityNum,money,email):
        self.userId = userId
        self.passwd = passwd
        self.name = name
        self.identityNum = identityNum
        self.money = money
        self.email = email
        self.lock = False
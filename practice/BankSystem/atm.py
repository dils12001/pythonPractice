from user import User
import pickle
import os
import myFunction

class ATM(object):
    allUserPath = os.path.join(os.getcwd(),'allUser.txt')
    def __init__(self):
        with open(self.allUserPath, 'rb') as f:
            self.allUser = pickle.load(f)   #紀錄用戶ID及實例{'123456':UserObject,...}
        #print(self.allUser)



    def createUser(self):
        name = input('請輸入用戶姓名:')
        while 1:
            passwd = input('請輸入用戶密碼:')
            if input('請再次輸入密碼:') == passwd:
                break
            print('兩次輸入不一致,請重新輸入...')
        identityNum = input('請輸入用戶身分證:')
        money = int(input('請輸入預存金額(高於$1000):'))
        if money < 1000:
            print('預存金額須高於$1000~')
            return -1
        email = input('請輸入用戶郵箱:')
        userId = myFunction.mkRandomUserId(self)

        newUser = User(userId,passwd,name,identityNum,money,email)
        self.allUser[userId] = newUser
        print('註冊成功')

    def deleteUser(self):
        userId = input('請輸入用戶ID:')
        if myFunction.accountVerify(self,userId):
            return -1

        del self.allUser[userId]
        print('您已成功註銷該用戶')

    def deposit(self):
        userId = input('請輸入用戶ID:')
        if myFunction.accountVerify(self, userId):
            return -1

        for i in range(2, -1, -1):
            saveMoney = int(input('請輸入存款金額(須大於$100):'))
            if saveMoney < 100:
                print('存款金額須高於$100,剩餘%d次輸入機會' % i)
                if i == 0:
                    return -1
                continue
            break

        self.allUser[userId].money += saveMoney
        print('存款成功,帳戶%s目前餘額為%d' % (self.allUser[userId].userId,self.allUser[userId].money))

    def withdraw(self):
        userId = input('請輸入用戶ID:')
        if myFunction.accountVerify(self, userId):
            return -1

        for i in range(2, -1, -1):
            getMoney = int(input('請輸入提款金額:'))
            if getMoney > self.allUser[userId].money:
                print('提款金額須低於您目前的餘額%d,剩餘%d次輸入機會' % (self.allUser[userId].money,i))
                if i == 0:
                    return -1
                continue
            break

        self.allUser[userId].money -= getMoney
        print('提款成功,帳戶%s目前餘額為%d' % (self.allUser[userId].userId,self.allUser[userId].money))

    def trafer(self):
        userId = input('請輸入用戶ID:')
        if myFunction.accountVerify(self, userId):
            return -1

        recieveUser = input('請輸入欲轉入之用戶Id:')
        if not self.allUser.get(recieveUser):
            print('該用戶ID不存在')
            return -1

        for i in range(2, -1, -1):
            transferMoney = int(input('請輸入轉帳金額(須大於$100):'))
            if transferMoney < 100:
                print('轉帳金額須高於$100,剩餘%d次輸入機會' % i)
                if i == 0:
                    return -1
                continue
            break

        self.allUser[recieveUser].money += transferMoney
        print(self.allUser[recieveUser].money)
        self.allUser[userId].money -= transferMoney
        print('轉帳成功,帳戶%s目前餘額為%d' % (self.allUser[userId].userId,self.allUser[userId].money))

    def searchImfo(self):
        print(self.allUser)
        userId = input('請輸入用戶ID:')
        if myFunction.accountVerify(self, userId):
            return -1

        theUser = self.allUser[userId]
        print('-----------------------------')
        print('用戶ID: %s' % userId)
        print('用戶姓名: %s' % theUser.name)
        print('用戶身分證: %s' % theUser.identityNum)
        print('帳戶餘額: %s' % theUser.money)
        print('用戶信箱: %s' % theUser.email)
        print('用戶是否鎖定: %s' % str(theUser.lock))
        input('請輸入任何值,以返回主畫面')

    def changePasswd(self):
        userId = input('請輸入用戶ID:')
        if myFunction.accountVerify(self, userId):
            return -1

        while 1:
            newPasswd = input('請輸入新密碼:')
            if input('請再次輸入密碼:') == newPasswd:
                break
            print('兩次輸入不一致,請重新輸入...')
        self.allUser[userId].passwd = newPasswd
        #print(self.allUser[userId].passwd)
        print('成功修改密碼')

    def lockUser(self):
        userId = input('請輸入用戶ID:')
        if not self.allUser.get(userId):
            print('該用戶ID不存在')
            return -1
        if myFunction.checkPasswd(self.allUser[userId].passwd):   #傳入該帳戶正確密碼 以檢查密碼輸入
            print('密碼輸入錯誤')
            return -1
        if self.allUser[userId].lock:
            print('該用戶已經被鎖定了...')
        else:
            self.allUser[userId].lock = True
            print('成功鎖定該用戶%s' % userId)

    def unlockUser(self):
        userId = input('請輸入用戶ID:')
        if not self.allUser.get(userId):
            print('該用戶ID不存在')
            return -1
        if myFunction.checkPasswd(self.allUser[userId].passwd):  # 傳入該帳戶正確密碼 以檢查密碼輸入
            print('密碼輸入錯誤')
            return -1
        if self.allUser[userId].lock:
            self.allUser[userId].lock = False
            print('成功解鎖該用戶%s' % userId)
        else:
            print('該用戶並沒有被鎖定...')

    def quit(self):
        with open(self.allUserPath, 'wb') as f:
            pickle.dump(self.allUser, f)
        print('正在退出系統,歡迎再次使用~')
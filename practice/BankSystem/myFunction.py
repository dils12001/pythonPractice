import random

def welcome():
    print('******************************')
    print('*      歡迎光臨土豪大銀行        *')
    print('******************************')


def showFunction():
    print('******************************')
    print('*   用戶註冊(1)   用戶註銷(2)   *')
    print('*    存款(3)       提款(4)     *')
    print('*    轉帳(5)   用戶資訊查詢(6)  *')
    print('*   密碼修改(7)   用戶鎖定(8)   *')
    print('*   用戶解鎖(9)     退出(0)    *')
    print('******************************')

def accountVerify(ATM,userId):
    if not ATM.allUser.get(userId):
        print('該用戶ID不存在')
        return -1
    if checkPasswd(ATM.allUser[userId].passwd):  # 傳入該帳戶正確密碼 以檢查密碼輸入
        print('密碼輸入錯誤')
        return -1
    if ATM.allUser[userId].lock:
        print('此用戶已被鎖定,請先解鎖該用戶再進行操作')
        return -1
    return 0

def checkPasswd(realPasswd):   #檢查密碼是否正確
    for i in range(2,-1,-1):
        temp = input('請輸入密碼:')
        if temp == realPasswd:
            print('輸入正確')
            return 0
        print('請輸入正確密碼,剩餘%d次輸入機會' %i)
    return -1

def mkRandomUserId(ATM):
    while 1:
        id = ''
        for i in range(6):
            id += str(random.randrange(0,9))
        if not ATM.allUser.get(id):    #檢查是否已存在該userId
            break
    print(id)
    return id
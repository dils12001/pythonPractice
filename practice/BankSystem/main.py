import myFunction
from atm import ATM
import time


def main():
    myFunction.welcome()
    adminUser = input('請輸入管理員帳號:')
    if adminUser != 'root':
        print('帳號錯誤!!')
        return -1
    adminPasswd = input('請輸入管理員密碼:')
    if adminPasswd != 'Zaq12wsx':
        print('密碼錯誤!!')
        return -1

    atm = ATM()
    print('登入中,請稍候...')

    while 1:
        time.sleep(2)
        myFunction.showFunction()
        action = input('請選擇操作(0~9):')

        if action == '1':
            if atm.createUser():
                print('註冊用戶失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '2':
            if atm.deleteUser():
                print('註銷用戶失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '3':
            if atm.deposit():
                print('存款失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '4':
            if atm.withdraw():
                print('提款失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '5':
            if atm.trafer():
                print('轉帳失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '6':
            if atm.searchImfo():
                print('查詢用戶資訊失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '7':
            if atm.changePasswd():
                print('修改用戶密碼失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '8':
            if atm.lockUser():
                print('鎖定用戶失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '9':
            if atm.unlockUser():
                print('解除用戶鎖定失敗...')
                print('重新載入畫面中...')
                continue
        elif action == '0':
            atm.quit()
            time.sleep(1)
            break
        else:
            print('請輸入有效操作碼==')

        print('重新載入畫面中...')


if __name__ == '__main__':
    main()


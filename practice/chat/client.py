import socket
import threading
import tkinter

usersLabel = {}
client = None

def chatWindow(user):
    print(user)

def recieve():
    global client
    while 1:
        info = client.recv(10240).decode('utf-8')
        print('***',info,'***')
        #最後一字符為'0'，則表示第一次連接回傳usersList
        if(info[-1] == '0'):
            usersList = info[:-1].split(',')
            global usersLabel
            for key in usersLabel:
                usersLabel[key].destroy()
                print(usersLabel[key])

            usersLabel = {}
            for i in range(len(usersList)):
                exec(usersList[i] + '=tkinter.Label(win, text="' + usersList[i] + '")')
                eval(usersList[i]).grid(row=4+i, column=1)
                eval(usersList[i]).bind("<Double-Button-1>", lambda event, user=usersList[i]:chatWindow(user))
                usersLabel[usersList[i]] = eval(usersList[i])

        # 最後一字符為'1'，則表示是 有user傳遞訊息過來
        elif(info[-1] == '1'):
            pass




def talk():
    global client
    while 1:
        data = input('say something:')
        client.send(data.encode('utf-8'))

def connectServer():
    global client
    ipStr = '127.0.0.1'#eIp.get()
    portStr = '8080'#ePort.get()
    #最後的'0'，表示是第一次連接，傳遞自己的userName
    userNameStr = eUserName.get() + '0'

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipStr, int(portStr)))
    # 連接伺服器(伺服器的IP,Port)

    client.send(userNameStr.encode('utf-8'))

    #創建 客戶端說話 的線程
    t = threading.Thread(target=talk)
    t.start()

    # 創建 客戶端接收訊息 的線程
    r = threading.Thread(target=recieve)
    r.start()

    for i in threading.enumerate():
        print(i,type(i))


    '''#另開 與另一人的單獨聊天視窗
    win = tkinter.Tk()
    win.title('chatClient')
    win.geometry('400x400+500+200')

    labelIp = tkinter.Label(win, text='ip')
    labelIp.grid(row=0, column=0)

    labelPort = tkinter.Label(win, text='port')
    labelPort.grid(row=1, column=0)

    win.mainloop()
    '''


win = tkinter.Tk()
win.title('connectServer')
win.geometry('240x250+500+200')

labelIp = tkinter.Label(win, text='Server IP:')
labelIp.grid(row=0, column=0)

labelPort = tkinter.Label(win, text='Server Port:')
labelPort.grid(row=1, column=0)

eIp = tkinter.Variable()
entryIp = tkinter.Entry(win, textvariable=eIp)
entryIp.grid(row=0, column=1)

ePort = tkinter.Variable()
entryPort = tkinter.Entry(win, textvariable=ePort)
entryPort.grid(row=1, column=1)

labelUserName = tkinter.Label(win, text='User Name:')
labelUserName.grid(row=2, column=0)

eUserName = tkinter.Variable()
entryUserName = tkinter.Entry(win, textvariable=eUserName)
entryUserName.grid(row=2, column=1)

buttonStart = tkinter.Button(win, text='連接伺服器', command=connectServer)
buttonStart.grid(row=3, column=1)

labelOnline = tkinter.Label(win, text='目前在線:')
labelOnline.grid(row=4, column=0)

#text = tkinter.Text(win, height=10, width=20)
#text.grid(row=4, column=1)

win.mainloop()

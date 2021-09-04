import socket
import threading
import tkinter

def connectServer():
    ipStr = eIp.get()
    portStr =  ePort.get()
    userNameStr = eUserName.get()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ipStr, int(portStr)))
    # 連接伺服器(伺服器的IP,Port)

    client.send(userNameStr.encode('utf-8'))

    def recieve():
        while 1:
            info = client.recv(1024)
            print(999)
            print('server said:' + info.decode('utf-8'))

    def talk():
        while 1:
            data = input('say something:')
            client.send(data.encode('utf-8'))


    #創建 客戶端說話 的線程
    t = threading.Thread(target=talk)
    t.start()

    # 創建 客戶端接收訊息 的線程
    r = threading.Thread(target=recieve)
    r.start()


    #
    win = tkinter.Tk()
    win.title('chatClient')
    win.geometry('400x400+500+200')

    labelIp = tkinter.Label(win, text='ip')
    labelIp.grid(row=0, column=0)

    labelPort = tkinter.Label(win, text='port')
    labelPort.grid(row=1, column=0)

    win.mainloop()



win = tkinter.Tk()
win.title('connectServer')
win.geometry('240x150+500+200')

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

text = tkinter.Text(win, height=1.4, width=20)
text.grid(row=4, column=1)

win.mainloop()

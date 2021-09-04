import tkinter
import socket
import threading

isFirstStart = True
isFirstConnect = True
user = {}


#對應每個User的Thread，來跑此函式run(clientSocket, clientAddress)
#回傳給每一客戶端 目前上線的 客戶端 dennis,Jack,fuck'
def run(clientSocket, clientAddress):
    global user
    #while 1:
    info = clientSocket.recv(1024).decode('utf-8')
    print(info)
    #最後一個字符為判斷符，'0'表示第一次連接(或重新連接)要求回傳在線的用戶列表
    if(info[-1] == '0'):
        userName = info[:-1]
        user[userName] = clientSocket
        print(user)
        connectUser = userName + str(clientAddress) + '連接成功...\n'
        text.insert(tkinter.INSERT, connectUser)

        #將List轉成字串 傳給 客戶端
        usersList = ','.join(list(user.keys())) + '0'
        user[userName].send(usersList.encode('utf-8'))
        #print('client said%s:' % str(clientAddress) + data.decode('utf-8'))
        #saySomething = input('to client:')
        #clientSocket.send(saySomething.encode('utf-8'))
    elif(info[-1] == '1'):
        pass

def start():
    global isFirstConnect
    ipStr = '127.0.0.1'#eIp.get()
    portStr = '8080'#ePort.get()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ipStr, int(portStr)))
    server.listen(5)

    strStartServer = '啟動伺服器...\n'
    text.insert(tkinter.END, strStartServer)

    while 1:
        clientSocket, clientAddress = server.accept()
        #為每個連線各創造一個線程
        #if(isFirstConnect):
        t = threading.Thread(target=run, args=(clientSocket, clientAddress))
        t.start()
        #isFirstConnect = False


def startServer():
    global isFirstStart
    if(isFirstStart):
        #控制是否是第一次按啟動按鈕
        isFirstStart = False
        s = threading.Thread(target=start)
        s.start()
    else:
        text.insert(tkinter.END, '伺服器已經啟動了...\n')
    #不能讓上面的while 1:放在這，因為會使主線程可再無線迴圈，這樣tkinter的視窗就當了
    #另開一線程等待處理無限迴圈(等待客戶端連接)



win = tkinter.Tk()
win.title('chatServer')
win.geometry('400x400+500+200')


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

buttonStart = tkinter.Button(win, text='啟動伺服器', command=startServer)
buttonStart.grid(row=2, column=1)

text = tkinter.Text(win, height=10, width=40)
text.grid(row=3, column=1)

win.mainloop()

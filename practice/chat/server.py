import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(('127.0.0.1',8080))

server.listen(5)
print('啟動伺服器...')

clientSocket, clientAddress = server.accept()
print(str(clientSocket) + '連接成功...')

while 1:
    data = clientSocket.recv(1024)
    print('client said%s:' % str(clientAddress) + data.decode('utf-8'))
    saySomething = input('to client:')
    clientSocket.send(saySomething.encode('utf-8'))


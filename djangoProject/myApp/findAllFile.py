import os
import collections
import time
#遍歷目錄
'''
#遞迴
def findAllFile1(path,space = ''):
    filesList = os.listdir(path)
    space += '\t'
    for file in filesList:
        absPath = os.path.join(path, file)
        if(os.path.isdir(absPath)):
            print('\033[1;36;1m'+space+file+'\033[0m')
            findAllFile1(absPath,space)
        else:
            print(space+file)


#stack
def findAllFile2(path):
    fileStack = []
    fileStack.append(path)
    while len(fileStack) != 0:
        filePath = fileStack.pop()
        for file in os.listdir(filePath):
            absPath = os.path.join(filePath, file)
            if(os.path.isdir(absPath)):
                print('\033[1;36;1m' + file + '\033[0m')
                fileStack.append(absPath)
            else:
                print(file)


#quene
def findAllFile3(path,space = ''):
    queue = collections.deque()
    queue.append(path)

    while len(queue) != 0:
        filePath = queue.popleft()
        for file in os.listdir(filePath):
            #抓出filePath底下的所有文件(目錄+檔案)
            absPath = os.path.join(filePath, file)
            #將所有文件(目錄+檔案)變成絕對路徑
            #是目錄就打印,再放進queue    檔案就直接打印
            if(os.path.isdir(absPath)):
                print('\033[1;36;1m' + file + '\033[0m')
                queue.append(absPath)
            else:
                print(file)
'''
'''
if __name__ == '__main__':
    #findAllFile1(r'E:\django\djangoProject')'''

a = time.perf_counter()
print(a)
time.sleep(2.5)
print(time.perf_counter())


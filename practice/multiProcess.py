from multiprocessing import Process
import time
import os

num = 100

def saySomething(str):
    print('子進程啟動...')
    print('子進程: '+ str + ' pid: %d' % os.getpid() + ' ppid: %d' % os.getppid())
    time.sleep(1.5)

    #使用全局變量num, 但全局變量在不同進程中 "不共享"
    global num
    num += 1
    print('子進程中的num = %d' % num)

    print('子進程結束...')

if __name__ == '__main__':
    print('父進程啟動...')
    p = Process(target=saySomething, args=('hello',))
    p.start()

    #父進程 等待子進程結束後 才結束
    p.join()

    print('父進程: world! pid: %d' % os.getpid())
    #全域變量 不共享
    print('父進程中的num = %d' % num)
    print('父進程結束...')


import threading

num = 0
#線程鎖
lock = threading.Lock()

def run(x):
    print('子線程啟動...' + str(threading.currentThread().name))
    global num
    for i in range(700000):
        #枷鎖
        """lock.acquire()
        try:
            num += x
            num -= x
        finally:
            #不管上面成功與否一定要釋放鎖
            lock.release()"""

        #同上代碼(建議用這，自動上鎖，自動解鎖)
        with lock:
            num += x
            num -= x


    print('子線程結束...num = %d' % num + str(threading.currentThread().name))

if __name__ == '__main__':
    print('主線程啟動...')
    t1 = threading.Thread(target=run, args=(2,))
    t2 = threading.Thread(target=run, args=(9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('主線程結束...num = %d' % num)

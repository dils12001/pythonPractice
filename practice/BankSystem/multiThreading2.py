import threading

num = 0

local = threading.local()

def run(addNum):
    local.x += addNum

def func(addNum):
    print('子線程啟動%s...' % (str(threading.currentThread().name)))
    #設置一個線程全域變量 local.x 將其值設置為真正的全域變量 num
    #在 "同一個" 線程內，local.x將作為全域變量 可被"該線程內"的任何函數調用
    #local.x的修改，將不會影響到全域變量num，也將不同線程中的local.x隔離開，不互相影響
    #即為各線程複製全域變量的值，並將其值作為各個線程的區域變數，與真正的區域變數之差別是，若同線程但不同函數間須使用同一個變量，不用將其值當作引述傳遞給另一函數，避免過多的引述傳遞
    local.x = num
    for i in range(10):
        run(addNum)
    print('子線程結束%s...num = %d' % (str(threading.currentThread().name),local.x))


if __name__ == '__main__':
    print('主線程啟動...')
    t1 = threading.Thread(target=func, args=(2,))
    t2 = threading.Thread(target=func, args=(9,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('主線程結束...num = %d' % num)
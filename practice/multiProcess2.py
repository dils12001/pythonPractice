import multiprocessing
import time,os,random

def saySomething(i):
    print('子進程%d啟動...%d' % (i, os.getpid()))

    start = time.time()
    time.sleep(random.choice([1,2,3]))
    end = time.time()

    print('子進程%s結束...耗時 %d' % (i, end-start))

if __name__ == '__main__':
    print('父進程啟動...')

    #獲取我的CPU執行緒，以我的電腦來說，2核4執行緒，即物理上是2核心，但intel捯超執行緒技術，使1核心模擬成2核心(2邏輯處理器)，所以邏輯上來說，我的電腦是4處理器(精確說是'執行緒')
    print(multiprocessing.cpu_count())
    print(os.cpu_count())

    #Pool(參數n) => 能同時執行n個進程，不加參數，則默認能同時執行4(my computer的邏輯處理器)個進程
    #參數n可超出我的最大執行緒，但就可能出現"併發"，而不是真的"並行"
    pp = multiprocessing.Pool(10)
    for i in range(10):
        pp.apply_async(saySomething, args=(i,))


    #使用Pool時，join()方法須在close()之後調用，並且close()之後，就不能在Pool中添加新進程
    pp.close()
    pp.join()

    print('父進程結束...')


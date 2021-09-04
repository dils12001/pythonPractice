import tkinter
import tkinter.messagebox
import tkinter.simpledialog

btnList = []

# 動態建立元件，並計算元件在窗體上的位置
def place(n):

    for i in range(n):
        exec('btn'+str(i)+'=tkinter.Button(root,text='+str(i)+')')
        eval('btn'+str(i)).place(x=80, y=10+i*30, width=60, height=20)
        btnList.append(eval('btn'+str(i)))
        #print(eval('btn'+str(i)))

    root.geometry('200x'+str((n)*30+70)+'+400+300')

    return n*30 + 10



# 建立tkinter應用程式
root = tkinter.Tk()

# 視窗標題
root.title('動態建立元件')

# 視窗初始大小和位置
root.geometry('200x180+400+300')

# 不允許改變視窗大小
root.resizable(False, False)



# 增加按鈕的按鈕
def btnSetClick():

    n = tkinter.simpledialog.askinteger(title='輸入一個整數', prompt='想動態增加幾個按鈕：', initialvalue=3)
    if n and n>0:
        startY = place(n)
        modify(startY)

        # 根據需要禁用和啟用“增加按鈕”和“清空按鈕”
        btnSet['state'] = 'disabled'
        btnClear['state'] = 'normal'

btnSet = tkinter.Button(root, text='增加按鈕', command=btnSetClick)


def btnClearClick():
    global btnList

    # 刪除動態建立的按鈕
    for btn in btnList:
        btn.destroy()

    btnList = []

    modify(20)

    btnClear['state'] = 'disabled'
    btnSet['state'] = 'normal'

btnClear = tkinter.Button(root,  text='清空按鈕', command=btnClearClick)

# 預設處於禁用狀態
btnClear['state'] = 'disabled'



# 動態調整“增加按鈕”和“清空按鈕”的位置
def modify(startY):
    btnSet.place(x=10, y=startY, width=80, height=20)
    btnClear.place(x=100, y=startY, width=80, height=20)

modify(20)

root.mainloop()







'''
class App:
    def __init__(self, root):
        root.title("打招呼测试")
        frame = tk.Frame(root)
        frame.pack()
        self.hi_there = tk.Button(frame, text="打招呼", fg="blue", command=self.say_hi)
        self.hi_there.pack(side=tk.LEFT)
    def say_hi(self):
        print("您刚才通过点击打招呼触发了我:大家好，我是badao！")
root = tk.Tk()
app = App(root)

root.mainloop()
'''
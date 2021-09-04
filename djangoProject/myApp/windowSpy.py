import win32con
import win32gui
import time
import win32com.client

'''
while 1:
    lineWindows = win32gui.FindWindow('CabinetWClass', '檔案總管')
    win32gui.ShowWindow(lineWindows, win32con.SW_HIDE)
    time.sleep(1)
    win32gui.ShowWindow(lineWindows, win32con.SW_SHOW)
    time.sleep(1)

'''

#lineWindows = win32gui.FindWindow('Qt5152QWindowIcon', 'LINE')
#win32gui.ShowWindow(lineWindows, win32con.SW_SHOW)

aa = win32com.client.Dispatch('SAPI.SPVOICE')
aa.Speak('aaaaaaaaaaaaaaaaaa')
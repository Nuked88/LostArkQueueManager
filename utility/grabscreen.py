import win32gui, win32ui, win32con, win32api
from ctypes import windll
from PIL import Image
import numpy as np
def grab_screen(hwin_code=0):
    hwnd = hwin_code
    if hwnd == 0:
        target="desktop"
    else:
        target="window"
    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    if target=="desktop":
        hwnd = win32gui.GetDesktopWindow()
        w = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        h = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        
    else:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    if target=="desktop":
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')

        img.shape = (h, w, 4)

        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
        win32gui.DeleteObject(saveBitMap.GetHandle())

    else:

        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)


        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)



        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')

        img.shape = (h, w, 4)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        if result != 1:
            #PrintWindow Succeeded
            im = None

    return img,w,h


def window_movetop(hwnd):
        win32gui.ShowWindow(hwnd,5)
        win32gui.SetForegroundWindow(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        return rect 

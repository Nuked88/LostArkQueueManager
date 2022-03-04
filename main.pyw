from time import sleep, time
from utility.grabscreen import grab_screen,window_movetop
from pathlib import Path
import win32gui
import cv2
from easyocr import Reader
import subprocess
import time
import mouse
import threading
import PySimpleGUI as sg
import yaml
import sys
import requests
#fix
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
# Set main path
main_path = Path(__file__).parent

#read configuration
with open(main_path/'config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


cache_screen = f"{main_path}\\targets\\screen.png"

start_control = False
start_game_and_control = False


if len(sys.argv)>1:
    if(sys.argv[1]=="c"):
        start_control = True
    elif sys.argv[1]=="gc":
        start_game_and_control = True


windows_list = []
def winEnumHandler( hwnd, ctx ):
    global windows_list
    if win32gui.IsWindowVisible( hwnd ):
        windows_list.append((hwnd, win32gui.GetWindowText( hwnd )))

def adjust_coord_fullscreen(x,y):
    import screeninfo
    monitors_data= screeninfo.get_monitors()
    subtract=0
    for monitor in monitors_data:
        if monitor.x<0:
            subtract= subtract+(abs(monitor.x))

    x = x-subtract
    return x,y


def find_image( image_full, image_to_find):
    # Using template matching to find the image
    image_full = cv2.imread(image_full)
    image_to_find = cv2.imread(image_to_find)
    res = cv2.matchTemplate(image_full, image_to_find, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)

    (startX, startY) = maxLoc
    endX = startX + image_to_find.shape[1]
    endY = startY + image_to_find.shape[0]
    if maxVal > 0.9:
        return [True,startX, startY, endX, endY]
    else:
        return [False,0,0,0,0]

def search_window(title_window):
    
    for hwnd, title in windows_list:
        if (title.find(title_window) != -1):
            return hwnd
           
    return None

def read_text(image,reader,search=""):
    fulltext = ""
    ocr_res = reader.readtext(image,batch_size=512)
    # join all the text
    #print(ocr_res)
    if search == "":
        for oc in ocr_res:
            fulltext = fulltext +" "+ oc[1]
    else:
        for oc in ocr_res:
            if oc[1].strip()==search:
                fulltext = oc[0]
                break
    
    return fulltext

def telegram_bot_sendtext(bot_message):
    if config["bot_chatID"] != "" or config["bot_chatID"] != None or config["bot_chatID"] != "None" or config["bot_chatID"] != "00000000":
        requests.post('https://laq.animecast.net/send_message', json={"queue":f"{bot_message}","serverName":"None","bot_chatID":config["bot_chatID"]})


def kill_myself():
    subprocess.call("taskkill /F /IM python.exe", shell=True)

def split_coord(coord):
    x = coord[1]
    y = coord[2]
    w = coord[3]
    h = coord[4]
    return x,y,w,h


def click(x,y):
    time.sleep(0.5)
    mouse.move(x, y)
    time.sleep(0.5)
    mouse.click()                      
def dclick(x,y):
    time.sleep(0.5)
    mouse.move(x, y) 
    mouse.double_click() 

def select_server(server_name):
    servers_pos = read_text(cache_screen,reader,server_name)
    #print(servers_pos[0])

    x=servers_pos[0][0]
    y=servers_pos[0][1]
    w=servers_pos[2][0]
    h=servers_pos[2][1]
 
    x = (x + w)/2
    y = (y + h)/2
    #print(x,y)
    dclick(x,y)

    sleep(2)
   

print("Loading OCR")
info = "Loading OCR"
reader = Reader(['en'], gpu=True)
info = "Loaded"
def run():
    global info
    global closeFromThread
    global started
    global reader
    # Load OCR

    print("Starting...")
    info = "Starting..."

    id=None
    while id is None and started:
        win32gui.EnumWindows( winEnumHandler, None )
        id = search_window("LOST")
        info="Process not found yet..."
        image,h,w = grab_screen(0)
        #save image
        cv2.imwrite(cache_screen,image)

        #if aec fail
        failed_load_image = find_image( cache_screen, f"{main_path}\\targets\\exit_eac.png")
        if failed_load_image[0]:
            info = "LostarK Failed to load"
            x,y,w,h = split_coord(failed_load_image)

            x = x + (w-x)/2
            y = y + (h-y)/2
            x,y = adjust_coord_fullscreen(x,y)
            click(x,y)
            sleep(10)
            info = "LostarK Failed waiting 10 seconds for reload..."
            subprocess.Popen("cmd /c start steam://run/1599340", start_new_session=True)

        time.sleep(1)  # wait 1 second
    try: 
        while started:
                try:  
                    info="Process found with id: "+str(id)+",Please select a server!"
                    image,h,w = grab_screen(hwin_code=id)
                    #save image
                    cv2.imwrite(cache_screen,image)


                    count_image_button = find_image(cache_screen, f"{main_path}\\targets\\button.png")

                    if(count_image_button[0] == True):

                        x,y,w,h = split_coord(count_image_button)

                        height =  h-y
                        width = w-x 
                        pointx =x
                        pointy= y-height*3
                        pointxext  = (x+width*2)
                        pointyext = y

                        crop_img = image[pointy:pointyext,pointx:pointxext]
                        

                        queue_spot = int(''.join(filter(str.isdigit, read_text(crop_img,reader))))


                        if queue_spot<config["send_message_under"]:
                            print(f"Queue is ending!({str(queue_spot)})", end ="\r")
                            info=f"Queue is ending!({str(queue_spot)})"
                            telegram_bot_sendtext(f"{str(queue_spot)} people")
                        else:
                            print(f"Queue is full({str(queue_spot)})", end ="\r")
                            info=f"Queue is full({str(queue_spot)})"


                            
                        
                        time.sleep(30)
                    else:
                        start_image_button = find_image(cache_screen, f"{main_path}\\targets\\launch.png")
        
                        if(start_image_button[0] == True):

                            x,y,w,h = split_coord(start_image_button)
                            
                            #cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
                            #click on center of rectangle
                            x = x + (w-x)/2
                            y = y + (h-y)/2

                            window_movetop(id)

                            click(x,y)

                            telegram_bot_sendtext("It's time to play!")
                            info="Session started! Closing window in 10 seconds"
                            time.sleep(10)
                            #kill 
                            closeFromThread = True
                            started = False

                        else:
                            info="Process found with id: "+str(id)+",Please select a server!"
                            if config["server_name"].strip()!="":
                                res = select_server(config["server_name"])
                                if res is None:
                                    info="Server not found, please select a server manually!"


                            
                except Exception as e:
                    print(e)
                    pass
        print("Closing thread")          
        info="Press Start"


    
    except Exception as e:
        print(e)



info="Press Start"
started=False
closeFromThread=False
sg.theme('Default1')   # Add a touch of color
# All the stuff inside your window.
fnt = 'Arial 15'
layout = [  [sg.Text('Loading...', font=fnt ,key='-INFO-')],
            [sg.Button('Start Game+Control', font=fnt ),sg.Button('Stop', font=fnt,disabled=True ), sg.Button('Start Control Only', font=fnt ),sg.Button('Cancel', font=fnt )] ]

# Create the Window
window = sg.Window('LostarK Queue Info', layout , location=(0,0))

input = window['-INFO-']
try:
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Cancel' or closeFromThread: # if user closes window or clicks cancel
            #kill thread
            started=False
            #t1.join()

            break
        if event == 'Start Game+Control' or start_game_and_control:
            start_game_and_control=False
            started=True
            subprocess.Popen("cmd /c start steam://run/1599340", start_new_session=True)
            t1 = threading.Thread(target=run, args=[])

            if not t1.is_alive():
                t1.start()

            print("Started")
            window['Start Game+Control'].Update(disabled=True)
            window['Start Control Only'].Update(disabled=True)
            window['Stop'].Update(disabled=False)

        if event == 'Start Control Only' or start_control:
            start_control=False
            started=True
            t1 = threading.Thread(target=run, args=[])
            
            if not t1.is_alive():
                t1.start()

            print("Started")
            window['Start Game+Control'].Update(disabled=True)
            window['Start Control Only'].Update(disabled=True)
            window['Stop'].Update(disabled=False)

        if event == 'Stop':
            start_control=False
            start_game_and_control=False
            started=False
            print("Stopped")
            window['Start Game+Control'].Update(disabled=False)
            window['Start Control Only'].Update(disabled=False)
            window['Stop'].Update(disabled=True)



        input.update(value=info)
            

    window.close()
    sleep(2)
    print("Closing")
    kill_myself()
except:
    pass
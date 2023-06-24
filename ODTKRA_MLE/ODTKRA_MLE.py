import argparse
from pynput.keyboard import Key, Controller
import win32gui
import psutil
import os
import time
from datetime import datetime

def focuswin(windowname="Oculus Debug Tool"):
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        
    pid = ""
    while True:
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        for i in top_windows:
            if windowname in i[1]:
                pid = i[0]
                win32gui.SetForegroundWindow(i[0])

        if pid == win32gui.GetForegroundWindow():
            break

def start_ODT(odt_path):
    
    os.startfile("\"" + odt_path + "OculusDebugTool.exe" + "\"")
    time.sleep(0.5)

    # Find the handle for the OculusDebugTool window
    window_handle = win32gui.FindWindow(None, "Oculus Debug Tool")

    if window_handle != 0:

        keyboard = Controller()
        win32gui.ShowWindow(window_handle, 5) #show window
        focuswin()
        
        for i in range(7):            
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            #print("down")


        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        #print("tab")

        #time.sleep(1)
        
        
        keyboard.press(Key.down)
        keyboard.release(Key.down)
        #print("down")


        win32gui.ShowWindow(window_handle, 0) #hide window
        focuswin()
    else:
        print("OculusDebugTool window not found.")
    
    return 0

def kill_ODT():

    #os.system("echo service set-pixels-per-display-pixel-override 1 | \"" + ODTPath + "OculusDebugToolCLI.exe" + "\"")

    for proc in psutil.process_iter():
        if proc.name() == "OculusDebugTool.exe":
            proc.kill()
    return 0

def check_ODT():
    for proc in psutil.process_iter():
        if proc.name() == "OculusDebugTool.exe":
            return True
    return False

def kb_macro():

    # Find the handle for the OculusDebugTool window
    window_handle = win32gui.FindWindow(None, "Oculus Debug Tool")

    if window_handle != 0:

        keyboard = Controller()

        win32gui.ShowWindow(window_handle, 5) #show window
        focuswin()

        #time.sleep(1)
        
        keyboard.press(Key.up)
        keyboard.release(Key.up)
        #print("up")

        #time.sleep(1)

        keyboard.press(Key.down)
        keyboard.release(Key.down)
        #print("down")

        #time.sleep(1)

        win32gui.ShowWindow(window_handle, 0) #hide window
        focuswin()
    else:
        print("OculusDebugTool window not found.")

    return 0

def get_pid():
    for proc in psutil.process_iter():
        if proc.name() == "OculusDebugTool.exe":
            pid = proc.pid
            return pid
            
def get_ram(pid):

    process = psutil.Process(pid)

    memory_info = process.memory_info()
    rss = memory_info.rss / 2**20

    return round(rss, 2)

if check_ODT():
    print("ODT is already running")
    print("Killing ODT")
    kill_ODT()
    
    
print("Starting ODT")
parser = argparse.ArgumentParser()
parser.add_argument('--odt-path', help='Path to OculusDebugTool.exe', default="C:\\Program Files\\Oculus\\Support\\oculus-diagnostics\\", type=str)
parser.add_argument('--leak-size', help='Define max leak size in MB', default=100, type=int)
parser.add_argument('--refresh-time', help='Define refresh time in minutes', default=9, type=int)

args = parser.parse_args()

os.system("echo service set-pixels-per-display-pixel-override 0.01 | \"" + args.odt_path + "OculusDebugToolCLI.exe" + "\"")

if args.odt_path != "C:\\Program Files\\Oculus\\Support\\oculus-diagnostics\\":
    print("Using custom path: " + args.odt_path)
    start_ODT(args.odt_path)
    print("ODT started")
else:
    start_ODT(args.odt_path)
    print("ODT started")


pid=get_pid()
start_time_refresh = time.time()
start_time_leak = time.time()
while True:
    time.sleep(0.5) #sleep for 0.5 seconds so you don't use 100% of your fucking CPU
    refresh_time = time.time() - start_time_refresh
    leak_time = time.time() - start_time_leak
    
    if leak_time >= 10:
        leak_size = get_ram(pid)
        print(datetime.now().strftime("%I:%M %p"),"| PID:", pid, "| odt is using", leak_size, "MB of RAM")

        if leak_size >= args.leak_size:
            print("MEMORY LEAK DETECTED!!!")
            print("KILLING ODT!!!")
            kill_ODT()
            
            print("Starting ODT!!!")
            start_ODT(args.odt_path)
            pid=get_pid()

        start_time_leak = time.time()
    
    if refresh_time >= args.refresh_time * 60:  

        print(datetime.now().strftime("%I:%M %p"), "| tracking refresh")
        kb_macro()
        start_time_refresh = time.time()

    
    

    

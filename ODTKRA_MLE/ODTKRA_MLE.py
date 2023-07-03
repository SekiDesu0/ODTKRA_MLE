import argparse
from pynput.keyboard import Key, Controller
import win32gui
import psutil
import os
import time
from datetime import datetime
import pyautogui
import ctypes
import sys


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
                #press a random ass key to fix some weird shit
                pyautogui.press("F13") #idek why this is needed but it is
                win32gui.SetForegroundWindow(i[0]) #just fucking work pleasee

        if pid == win32gui.GetForegroundWindow():
            break

def start_ODT(odt_path):
    
    os.startfile("\"" + odt_path + "OculusDebugTool.exe" + "\"")
    time.sleep(0.1) #idek if this is necessary but i'll leave it just in case 

    # Find the handle for the OculusDebugTool window
    window_handle = win32gui.FindWindow(None, "Oculus Debug Tool")

    #may or may not change this later
    if window_handle != 0:

        keyboard = Controller()
        win32gui.ShowWindow(window_handle, 5) #show window
        focuswin()
        
        for i in range(6):    
            #time.sleep(1)        
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            #print("down")

        #time.sleep(1)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        #print("tab")

        #time.sleep(1)
        keyboard.press(Key.up)
        keyboard.release(Key.up)
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

def kill_ODT(exit):
    
    if exit == True: #if the program is exiting then set the resolution back to 1
        os.system("echo service set-pixels-per-display-pixel-override 1 | \"" + args.odt_path + "OculusDebugToolCLI.exe" + "\"")
        print("shit worked")

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

#should i even use this
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

def format_time(milliseconds):
    seconds = milliseconds // 1000  # Convert milliseconds to seconds
    minutes = seconds // 60  # Calculate the number of minutes
    seconds %= 60  # Calculate the remaining seconds

    return f"{minutes:02d}:{seconds:02d}"  # Format minutes and seconds with leading zeros if necessary

#i stole this
def cleanup():
    # Code to be executed when the process is terminated or window is closed
    kill_ODT(True)
    sys.exit(0)  # Terminate the program gracefully
    
#i stole this too   
def console_ctrl_handler(ctrl_type):
    if ctrl_type == 2:  # Ctrl + C event
        cleanup()
        return True
    elif ctrl_type == 5:  # Close event
        cleanup()
        return True
    return False
    

if __name__ == "__main__":
    #set console size because why not
    #ctypes.windll.kernel32.SetConsoleWindowInfo(ctypes.windll.kernel32.GetStdHandle(-11), True, ctypes.byref(ctypes.wintypes.SMALL_RECT(0, 0, 300 - 1, 50 - 1)))
    
    # I didn't totally steal this from the original ODTKRA
    print("ODTKRA uses Oculus Debug Tool to keep your rift alive.\n It is basically a \"advanced macro\", \nwhich means you interacting with the debug tool can cause ODTKRA to fail. \n If ODTKRA stops working then close and reopen it.")
    print("The Oculus Debug Tool is supposed to be minimized, let it stay so.")
    print("\nThis program changes the resolution of the Rift CV1 to a very low amount, it will be reversed when program exits or when computer restarts.")
    print("\nLog:")

    #start by killing ODT if it is already running
    if check_ODT():
        print("ODT is already running")
        print("Killing ODT")
        kill_ODT(False)
        
        
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--odt-path', help='Path to OculusDebugTool.exe', default="C:\\Program Files\\Oculus\\Support\\oculus-diagnostics\\", type=str)
    parser.add_argument('--leak-size', help='Define max leak size in MB', default=512, type=int)
    parser.add_argument('--refresh-time', help='Define refresh time in minutes', default=10, type=int)

    args = parser.parse_args()

    #set resolution to 0.01
    os.system("echo service set-pixels-per-display-pixel-override 0.01 | \"" + args.odt_path + "OculusDebugToolCLI.exe" + "\"")
    print("Resolution set to 0.01")
    ctypes.windll.kernel32.SetConsoleTitleW("ODTKRA_MLE")

    #start ODT
    print("|", datetime.now().strftime("%I:%M %p"), "| Starting ODT! |")
    start_ODT(args.odt_path)
    print("|", datetime.now().strftime("%I:%M %p"), "| ODT started!  |")
  

    #start super advanced macro
    pid=get_pid()
    start_time_refresh = time.time()
    start_time_leak = time.time()
    refresh_count = 0
    leak_count = 0
    
    while True:
        #i stole this and don't even know how it works
        # Set the console control handler to terminate the program
        if sys.platform == 'win32':
            # Windows-specific code
            kernel32 = ctypes.windll.kernel32
            SetConsoleCtrlHandler = kernel32.SetConsoleCtrlHandler
            CTRL_C_EVENT = 0  # Ctrl + C event
            CTRL_CLOSE_EVENT = 2  # Close event

            # Create the callback function type
            ConsoleCtrlHandlerType = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_uint)

            # Create the callback function instance
            console_ctrl_handler_func = ConsoleCtrlHandlerType(console_ctrl_handler)

            # Register the console control handler
            SetConsoleCtrlHandler(console_ctrl_handler_func, True)
            
        
        #start of the janky ass shit    
        time.sleep(0.1) #sleep for 0.1 seconds so you don't use 100% of your fucking CPU
        refresh_time = time.time() - start_time_refresh
        leak_time = time.time() - start_time_leak
        
        if leak_time >= 1:
            leak_size = get_ram(pid)
            print("|", datetime.now().strftime("%I:%M %p"),"| PID:", pid, "| ODT is using", format(leak_size, ".2f"), "MB of RAM |", format_time(int(args.refresh_time*60000 - refresh_time*1000)), "Until tracking refresh | Refresh count:", refresh_count, "| Leak count:", leak_count, "|")
            
            
            if leak_size >= args.leak_size:
                print("|", datetime.now().strftime("%I:%M %p"), "| MEMORY LEAK DETECTED! |")
                print("|", datetime.now().strftime("%I:%M %p"), "| KILLING ODT! |")
                kill_ODT(False)
                
                print("|", datetime.now().strftime("%I:%M %p"), "| Starting ODT! |")
                start_ODT(args.odt_path)
                
                pid=get_pid()
                leak_count+=1

            start_time_leak = time.time()
        
        if refresh_time >= args.refresh_time * 60:  

            print("|", datetime.now().strftime("%I:%M %p"), "| Tracking Refreshed! |")
            kb_macro()
            start_time_refresh = time.time()
            refresh_count+=1

    
    

    

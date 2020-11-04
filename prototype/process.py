import win32gui, win32com.client
import win32process
import psutil
from collections import namedtuple

ProcessInfo = namedtuple("ProcessInfo", ['pid', 'name', 'handle'])

class ProcessState:
    '''Class for requesting current current running processes '''

    def __init__(self, update_interval=0):
        # update_interval not used yet
        self._process_list = []
        self._lookup = {p.pid: p.info['name'] for p in psutil.process_iter(['name'])}

    ''' Current_processes returns a list of currently running processes '''
    def current_processes(self):
        self._process_list = []
        win32gui.EnumWindows(self._callback, self._process_list)
        return list(self._process_list)


    ''' win32 callback function. Gets called till False is returned or finished'''
    def _callback(self, handle, process_list):
        if self._is_main_window(handle):
            _threadId, processId = win32process.GetWindowThreadProcessId(handle)
            process_name = self._lookup.get(processId, "ProcessId Not found")
            p = ProcessInfo(processId, process_name, handle)
            process_list.append(p)


    ''' returns True if handle is a mainwindow '''
    def _is_main_window(self, handle):
        return win32gui.GetWindow(handle, 4) == 0 and win32gui.IsWindowVisible(handle);



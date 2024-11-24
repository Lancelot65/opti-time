# src/screen_time.py

from time import time, sleep
import ctypes
import psutil
from .manage_db import database

"""
TODO
- [ ] faire le temps d'écran des site utiliser

- [ ] rajouter des option dans le exe
- [ ] fonctionnalité de blocage d'app + site web
- [ ] compatibilité entre les fichier pour éviter les doubles appels
"""


class screen_time:
    def __init__(self) -> None:
        self.db = database()
    
    @staticmethod
    def get_use_application():
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process = psutil.Process(pid.value)
        return process.name().split('.')[0]

    def add_time(self, name : str):
        self.db.update_table(name)
    
    def update(self):
        self.add_time(screen_time.get_use_application())
    
    def loop(self):
        past_time = time()
        while True:
            sleep(max(0, 1 - (time() - past_time)))
            self.update()
            past_time = time()
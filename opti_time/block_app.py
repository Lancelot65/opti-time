# src/block_app.py

import os
import ctypes
from pathlib import Path
import json
from time import sleep

NOT_FIND = 1
OK = 0

# [ ] faire la classe settings mais modéliser avant

class setting:
    def __init__(self) -> None:
        if os.path.exists('.setting.json'):
            
            with open('.setting.json', 'r') as fichier:
                self.data = json.load(fichier)
        
        else:
            self.data = {}
            self.save()
        
    def save(self):
        with open('.setting.json', 'w') as fichier:
            json.dump(self.data, fichier, indent=4)
    
    def find_path(self, app_name):
        start_dir = Path.home() / "AppData" / "Local"
        temp = ""
        for path in start_dir.rglob(app_name):
            temp = path
                    
        if temp:
            return str(temp)
        else:
            print(f"{app_name} path was not found please presice the path in the setting")
            return NOT_FIND
    
    def add_app(self, app_name):
        # path = self.find_path(app_name)
        # if path == NOT_FIND:
        #     # - gérer cette exception et demander un path puis le vérifier
        #     return NOT_FIND
        self.data[app_name] = {'block' : True, 'path' : None}
        self.save()
    
    def remove_app(self, app_name):
        if app_name not in self.data:
            return NOT_FIND
        else:
            self.data.pop(app_name)
            self.save()
            return OK
    
    def is_block(self, app_name):
        return self.data[app_name]['block']

    
    def day_change(self):
        for app in self.data:
            self.data[app]['block'] = True
        self.save()
    
    def disable_block(self, app_name):
        if app_name not in self.data:
            print("app not in _settings")
            return NOT_FIND
        else:
            self.data[app_name]['block'] = False
            self.save()
            return OK
    
    def get_app(self):
        return [app for app in self.data]
        

class block_app:
    def __init__(self) -> None:
        self.setting = setting()    
    
   
    def loop(self):
        while True:
            self.update()    
        
    def update(self):
        tasklist = os.popen('tasklist').read()
        for app in self.setting.data:
            if self.setting.is_block(app):
                if app.lower() in tasklist.lower():                    
                    user_response = ctypes.windll.user32.MessageBoxW(0, f"{app} is block, are you sre to continue", "Time limit", 4)
                    if user_response == 6:
                        self.setting.disable_block(app)
                    elif user_response == 7:
                        os.system(f'taskkill /f /im {app}') 
                        sleep(1) # wait end of kill proces
        # make a version wo the app doesn't start
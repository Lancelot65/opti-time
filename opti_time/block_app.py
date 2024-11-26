# src/block_app.py

import os
import ctypes
from pathlib import Path
import json
from time import sleep

NOT_FIND = 1
OK = 0

class setting:
    def __init__(self) -> None:
        """
        Initializes the settings by loading data from '.setting.json'.
        If the file does not exist, it creates an empty settings file.
        """
        if os.path.exists('.setting.json'):
            with open('.setting.json', 'r') as fichier:
                self.data = json.load(fichier)
                if self.data is None:  # Vérifiez si les données chargées sont None
                    self.data = {}
        else:
            self.data = {}
            self.save()
        
    def save(self):
        """
        Saves the current settings data to '.setting.json'.
        """
        with open('.setting.json', 'w') as fichier:
            json.dump(self.data, fichier, indent=4)
    
    def find_path(self, app_name: str):
        """
        Searches for the path of the specified application in the local AppData directory.

        Args:
            app_name (str): The name of the application to find.

        Returns:
            str: The path of the application if found, otherwise a NOT_FIND constant.
        """
        start_dir = Path.home() / "AppData" / "Local"
        temp = ""
        for path in start_dir.rglob(app_name):
            temp = path
                    
        if temp:
            return str(temp)
        else:
            print(f"{app_name} path was not found, please specify the path in the settings.")
            return NOT_FIND
    
    def add_app(self, app_name: str):
        """
        Adds a new application to the settings with a default block status.

        Args:
            app_name (str): The name of the application to add.
        """
        self.data[app_name] = {'block': True, 'path': None}
        self.save()
    
    def remove_app(self, app_name: str):
        """
        Removes an application from the settings.

        Args:
            app_name (str): The name of the application to remove.

        Returns:
            int: OK if the application was removed, NOT_FIND if the application was not found.
        """
        if app_name not in self.data:
            return NOT_FIND
        else:
            self.data.pop(app_name)
            self.save()
            return OK
    
    def is_block(self, app_name: str):
        """
        Checks if the specified application is blocked.

        Args:
            app_name (str): The name of the application to check.

        Returns:
            bool: True if the application is blocked, False otherwise.
        """
        return self.data[app_name]['block']

    def day_change(self):
        """
        Resets the block status of all applications to True.
        """
        for app in self.data:
            self.data[app]['block'] = True
        self.save()
    
    def disable_block(self, app_name: str):
        """
        Disables the block status for the specified application.

        Args:
            app_name (str): The name of the application to disable blocking.

        Returns:
            int: OK if the block was disabled, NOT_FIND if the application was not found.
        """
        if app_name not in self.data:
            print("App not in settings.")
            return NOT_FIND
        else:
            self.data[app_name]['block'] = False
            self.save()
            return OK
    
    def get_app(self):
        """
        Retrieves a list of all applications in the settings.

        Returns:
            list: A list of application names.
        """
        return [app for app in self.data]
        

class block_app:
    def __init__(self) -> None:
        """
        Initializes the block_app class and its settings.
        """
        self.setting = setting()    
    
    def loop(self) -> None:
        """
        Starts the main loop for monitoring and updating application statuses.
        """
        while True:
            self.update()    
        
    def update(self) -> None:
        """
        Checks the current task list and manages application blocking based on settings.
        """
        tasklist = os.popen('tasklist').read()
        for app in self.setting.data:
            if self.setting.is_block(app):
                if app.lower() in tasklist.lower():                    
                    user_response = ctypes.windll.user32.MessageBoxW(0, f"{app} is blocked, are you sure to continue?", "Time limit", 4)
                    if user_response == 6:
                        self.setting.disable_block(app)
                    elif user_response == 7:
                        try:
                            os.system(f'taskkill /f /im {app}') 
                            sleep(1)  # wait for the process to end
                        except Exception as e:
                            print(f"An error occurred while trying to kill the process {app}: {e}")
        # make a version where the app doesn't start

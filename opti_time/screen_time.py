# src/screen_time.py

from time import time, sleep
import ctypes
import psutil
from .manage_db import database

class screen_time:
    def __init__(self) -> None:
        """
        Initializes the screen_time class and creates a database instance.

        This constructor initializes the database connection for tracking screen time.
        """
        self.db = database()
    
    @staticmethod
    def get_use_application() -> str:
        """
        Retrieves the name of the currently active application.

        Returns:
            str: The name of the currently active application without its extension.

        Raises:
            Exception: If there is an error retrieving the active application name.
        """
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            process = psutil.Process(pid.value)
            return process.name().split('.')[0]
        except Exception as e:
            raise Exception(f"Error retrieving active application: {e}")

    def add_time(self, name: str):
        """
        Adds screen time for the specified application name.

        Args:
            name (str): The name of the application to update the screen time for.

        Raises:
            Exception: If there is an error updating the time in the database.
        """
        try:
            self.db.update_table(name)
        except Exception as e:
            raise Exception(f"Error adding time for {name}: {e}")
    
    def update(self):
        """
        Updates the screen time for the currently active application.

        Raises:
            Exception: If there is an error updating the time for the active application.
        """
        try:
            return self.add_time(screen_time.get_use_application())
        except Exception as e:
            raise Exception(f"Error updating screen time: {e}")
    
    def loop(self):
        """
        Continuously tracks and updates the screen time for the active application.

        This method runs an infinite loop that updates the screen time every second.
        
        Raises:
            Exception: If there is an error during the update process.
        """
        past_time = time()
        while True:
            sleep(max(0, 1 - (time() - past_time)))
            self.update()
            past_time = time()

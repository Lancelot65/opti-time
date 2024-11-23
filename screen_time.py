from time import time, sleep
import ctypes
import psutil
import sqlite3
from datetime import datetime, timedelta

"""
TODO
- [x] main loop with 1s wait
- [x] func for get use it application in front off 
- [x] add auto save into sql base or other
- [x] auto save every x second
- [x] check if day change
- [ ] exploiter la db
- [ ] rajouter des option dans le exe
- [ ] reorganiser le print
- [ ] ajouter des -func au python mon.py
- [ ] faire le temps d'écran des site utiliser
- [ ] fonctionnalité de blocage d'app + site web
- faire deja un optisail.screen_time


- [ ] passer en c++ ???
"""

class bcolors:
    HEADER = '\033[95m'
    BLACK = '\033[90m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class database:
    def __init__(self, database_name = "screen_time.db") -> None:
        self.con = sqlite3.connect(database_name)
        self.cur = self.con.cursor()
        self.table_name = datetime.today().strftime("%Y-%m-%d")
        
        self.create_table()
         
    def create_table(self):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS \"{self.table_name}\" ( \
                           name TEXT NOT NULL, \
                           time INTEGER NOT NULL \
                           )")
    
    def check_if_day_change(self):
        if datetime.today().strftime("%Y-%m-%d") != self.table_name:
            self.table_name = datetime.today().strftime("%Y-%m-%d")
            self.create_table()
        
    def update_table(self, name : str):
        self.check_if_day_change()
        self.cur.execute(f"SELECT time FROM \"{self.table_name}\" WHERE name = ?", (name,))
        row = self.cur.fetchone()

        # Vérifier si la ligne existe
        if row:
            # Si la ligne existe, incrémenter le time
            new_time = row[0] + 1
            self.cur.execute(f"UPDATE \"{self.table_name}\" SET time = ? WHERE name = ?", (new_time, name))
        else:
            # Si la ligne n'existe pas, créer une nouvelle ligne avec time = 1
            self.cur.execute(f"INSERT INTO \"{self.table_name}\" (name, time) VALUES (?, ?)", (name, 1))

        self.con.commit()

    def __del__(self):
        self.cur.close()
        self.con.close()
        print('db close')           
     
    def get_all_table(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cur.fetchall()      
 
class check_time_loop:
    def __init__(self) -> None:
        self.db = database()
    
    def get_use_application(self):
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process = psutil.Process(pid.value)
        return process.name().split('.')[0]

    def add_time(self, name : str):
        self.db.update_table(name)
    
    def stop_by_user(self):
        try:
            self.loop()
        except KeyboardInterrupt:
            print("\nLe programme a été arrêté par l'utilisateur.")
        
    def loop(self):
        past_time = time()
        while True:
            
            sleep(1 - (time() - past_time))
            self.add_time(self.get_use_application())
            past_time = time()


    
class tools:
    def __init__(self) -> None:
        db = database()
        self.tables = db.get_all_table()
        self.json = {}
        for table in self.tables:
            resultats = db.cur.execute(f"SELECT name, time FROM \"{table[0]}\"").fetchall()
        
            dictionnaire = {nom: time for nom, time in resultats}
            self.json[table[0]] = dictionnaire
    
    def get_formated_time(self, secondes):
        
        t = timedelta(seconds=secondes)
        
        heures, reste = divmod(t.total_seconds(), 3600)
        minutes, secondes = divmod(reste, 60)
        
        return int(heures), int(minutes), int(secondes)
    
    
    
    def print(self, date):
        for app in self.json[date]:
            heures, minutes, secondes = self.get_formated_time(self.json[date][app])
            print(f"{bcolors.CYAN}{app:<10}{bcolors.ENDC}{bcolors.BLACK}{f'{heures:02}h {minutes:02}m {secondes:02}s':<15}{bcolors.ENDC}")
            # print(app, "   ", )
    
    def all_print(self):
        total = 0
        for app in self.json[datetime.today().strftime("%Y-%m-%d")]:
            total += self.json[datetime.today().strftime("%Y-%m-%d")][app]
        heures, minutes, secondes = self.get_formated_time(total)
        print(f"{bcolors.BOLD}Day's screen-time{bcolors.ENDC}", f"{f"{heures:23}h {minutes:02}m {secondes:02}s":<15}")
        print("─"*50)
        
        self.print(datetime.today().strftime("%Y-%m-%d"))
        
        print("─"*50)
        

# tools().all_print()
check_time_loop().stop_by_user()
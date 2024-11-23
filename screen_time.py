from time import time, sleep
import ctypes
import psutil
import sqlite3
from datetime import datetime, timedelta

"""
TODO
- [x] exploiter la db
- [ ] rajouter des option dans le exe
- [x] reorganiser le print
- [ ] ajouter des -func au python mon.py
- [ ] faire le temps d'écran des site utiliser
- [ ] fonctionnalité de blocage d'app + site web
- [ ] faire deja un optisail.screen_time
- [ ] passer en datetime eet pas en formatter
- [ ] rajouter plus de détails dans le full week



- [ ] passer en c++ ???
"""

class bcolors:
    HEADER = '\033[95m'
    BLACK = '\033[90m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

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
    
    def return_data(self):
        TABLES = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        output = {}
        for table in TABLES:
            resultats = self.cur.execute(f"SELECT name, time FROM \"{table[0]}\"").fetchall()
            temp = {nom: time for nom, time in resultats}
            output[table[0]] = temp
        return output

    def __del__(self):
        self.cur.close()
        self.con.close()
    
 
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
        self.data = db.return_data() 
    
    def get_formated_time(self, seconds):
        t = timedelta(seconds=seconds)
        hours, reste = divmod(t.total_seconds(), 3600)
        minutes, seconds = divmod(reste, 60)
        return f"{f'{int(hours):02}h {int(minutes):02}m {int(seconds):02}s':<15}"

    def sum_day(self, day):
        if not day in self.data:
            print(f"{day} is not in the database")
            return 0
        sum = 0
        for app in self.data[day]:
            sum += self.data[day][app]
        return sum
    
    def sum_week(self, day):
        output = 0
        monday_date = self.get_previous_monday(day)
        for i in range(7):
            output += self.sum_day(((monday_date + timedelta(days=i)).strftime('%Y-%m-%d')))
        return output
        
    def print_day(self, day):
        if not day in self.data:
            print(f"{day} is not in the database")
            return
        print(f"Day's screen-time {21*' '}{bcolors.BLACK}{self.get_formated_time(self.sum_day(day))}{bcolors.ENDC}")
        print("─"*50)
        for app in self.data[day]:
            print(f"{bcolors.CYAN}{app:<39}{bcolors.ENDC}{bcolors.BLACK}{self.get_formated_time(self.data[day][app])}{bcolors.ENDC}")

        print("─"*50)
        
    
    def get_previous_monday(self, date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        days_to_monday = date_obj.weekday() % 7
        previous_monday = date_obj - timedelta(days=days_to_monday)    
        return previous_monday
    
    def print_week(self, date_str):
        print(f"Week's screen-time {20*' '}{bcolors.BLACK}{self.get_formated_time(self.sum_week(date_str))}{bcolors.ENDC}")
        print("─"*50)
        
        monday_date = self.get_previous_monday(date_str)
        for i in range(7):
            days = monday_date + timedelta(days=i)
            print(f"{bcolors.BLUE}{days.strftime('%a')}{bcolors.ENDC}"      , end='   ')
            print(f"{bcolors.CYAN}{days.strftime('%y-%m-%d')}{bcolors.ENDC}", end=25*' ')
            
            if days.strftime('%Y-%m-%d') in self.data:
                print(f"{bcolors.BLACK}{self.get_formated_time(self.sum_day(days.strftime('%Y-%m-%d')))}{bcolors.ENDC}")
            else:
                print(f"{bcolors.BLACK}00h 00m 00s{bcolors.ENDC}")
        print("─"*50)
        
        

tools().print_day('2024-11-23')

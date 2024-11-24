from .manage_db import database
from datetime import timedelta, datetime

INVALID_FORMAT = 2
INVALID_DAY = 1
OK = 0

class _bcolors:
    HEADER = '\033[95m'
    BLACK = '\033[90m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
class displays:
    def __init__(self) -> None:
        self.data = database().return_data() 
    
    @staticmethod
    def get_formated_time(seconds):
        t = timedelta(seconds=seconds)
        hours, reste = divmod(t.total_seconds(), 3600)
        minutes, seconds = divmod(reste, 60)
        return f"{f'{int(hours):02}h {int(minutes):02}m {int(seconds):02}s':<15}"

    @staticmethod
    def get_previous_monday(date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        days_to_monday = date_obj.weekday() % 7
        previous_monday = date_obj - timedelta(days=days_to_monday)    
        return previous_monday

    @staticmethod
    def check_date(date_str):
        try:
            date = datetime.strptime(date_str, '%y-%m-%d')
            return INVALID_FORMAT
        except ValueError:
            return OK

    def sum_day(self, day, print_day=False):
        if not day in self.data:
            return 0
        return sum(self.data[day].values())
    
    def sum_week(self, day):
        monday_date = self.get_previous_monday(day)
        return sum(self.sum_day((monday_date + timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(7))
        
    def print_day(self, day):
        if displays.check_date == INVALID_FORMAT:
            return INVALID_FORMAT
        if day not in self.data:
            return INVALID_DAY
        
        print("─"*50)
        print(f"Day's screen-time {21*' '}{_bcolors.BLACK}{displays.get_formated_time(self.sum_day(day))}{_bcolors.ENDC}")
        print("─"*50)
        for app in self.data[day]:
            print(f"{_bcolors.CYAN}{app:<39}{_bcolors.ENDC}{_bcolors.BLACK}{displays.get_formated_time(self.data[day][app])}{_bcolors.ENDC}")

        print("─"*50)
    
    def print_week(self, date_str):
        
        
        if displays.check_date == INVALID_FORMAT:
            return INVALID_FORMAT
        
        print("─"*50)
        print(f"{_bcolors.GREEN}Week's screen-time{_bcolors.ENDC} {20*' '}{_bcolors.BLACK}{displays.get_formated_time(self.sum_week(date_str))}{_bcolors.ENDC}")
        print("─"*50)
        
        monday_date = displays.get_previous_monday(date_str)
        for i in range(7):
            days = monday_date + timedelta(days=i)
            print(f"{_bcolors.BLUE}{days.strftime('%a')}{_bcolors.ENDC}"      , end='   ')
            print(f"{_bcolors.CYAN}{days.strftime('%y-%m-%d')}{_bcolors.ENDC}", end=25*' ')
            
            if days.strftime('%Y-%m-%d') in self.data:
                print(f"{_bcolors.BLACK}{displays.get_formated_time(self.sum_day(days.strftime('%Y-%m-%d')))}{_bcolors.ENDC}")
            else:
                print(f"{_bcolors.BLACK}00h 00m 00s{_bcolors.ENDC}")
        print("─"*50)
        total_usage = {}

        # Itérer sur les 7 jours à partir de la date de début
        for i in range(7):
            current_date = (monday_date + timedelta(days=i)).strftime('%Y-%m-%d')
            
            if current_date in self.data:
                for app, time in self.data[current_date].items():
                    if app not in total_usage:
                        total_usage[app] = 0
                    total_usage[app] += time

        # Afficher le temps d'écran total pour chaque application
        print(f"{_bcolors.GREEN}App screen-time{_bcolors.ENDC}")
        print("─"*50)
        for app, total_time in total_usage.items():
            print(f"{_bcolors.CYAN}{app:<39}{_bcolors.ENDC}{_bcolors.BLACK}{displays.get_formated_time(total_time)}{_bcolors.ENDC}")
        print("─"*50)
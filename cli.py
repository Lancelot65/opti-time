import argparse
from datetime import datetime
from opti_time.display import displays, INVALID_DAY, INVALID_FORMAT
from opti_time.block_app import setting, NOT_FIND, OK, block_app
from opti_time.screen_time import screen_time
from time import time, sleep

"""TODO
- [ ] Better interface
"""

parser = argparse.ArgumentParser(description='Opti_time')

default_date = datetime.now().strftime("%Y-%m-%d")

parser.add_argument('--day_time', '-dt', type=str, help='date (default=now)')
parser.add_argument('--week_time', '-wt', type=str, help='date (default=now)')
parser.add_argument('--remove_app', '-ra', type=str)
parser.add_argument('--add_app', '-aa', type=str)
parser.add_argument('--get_app', '-ga')
parser.add_argument('--start_time', '-st')
parser.add_argument('--start_block', '-sb')
parser.add_argument('--start_all', '-sa')


args = parser.parse_args()

display = displays()
if args.day_time is not None:
    day_time = args.day_time if args.day_time != 'now' else datetime.now().strftime("%Y-%m-%d")
    output = display.print_day(day_time)
    if output == INVALID_FORMAT:
        print(f"The format is not respect (years-month-day) -> {datetime.now().strftime("%Y-%m-%d")}")
    elif output == INVALID_DAY:
        print("NOTE : You don't have data in this day")

# Vérifier si week_time a été fourni
if args.week_time is not None:
    # Si une valeur est fournie, l'utiliser, sinon utiliser la date par défaut
    week_time = args.week_time if args.week_time != 'now' else datetime.now().strftime("%Y-%m-%d")
    output = display.print_week(week_time)
    
    if output == INVALID_FORMAT:
        print(f"The format is not respect (years-month-day) -> {datetime.now().strftime("%Y-%m-%d")}")

    
if args.remove_app:
    if setting().remove_app(args.remove_app) == NOT_FIND:
        print(f"The application {args.remove_app} is not in the setting")
        
if args.add_app:
    setting().add_app(args.add_app)
    
if args.get_app:
    print(setting().get_app())
    
if args.start_time:
    pass
    # lancer la boucle
    # screen_time().loop()

if args.start_block:
    pass
    # lancer la boucle
    # block_app().loop()

if args.start_all:
    pass

    # block_app_ = block_app()
    # screen_time_ = screen_time()
    # while True:
    #     sleep(max(0, 1 - (time() - past_time)))
    #     block_app_.update()
    #     screen_time_.update()
    #     past_time = time()
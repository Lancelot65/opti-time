from opti_time.screen_time import screen_time
import json
import os
import atexit
import sys

def load_settings():
    with open('.loop.json', 'r') as fichier:
        return json.load(fichier)
    
data = load_settings()

def save_settings(data):
    with open('.loop.json', 'w') as fichier:
        json.dump(data, fichier, indent=4)

def clean_PID():
    data['PID_time'] = None
    save_settings(data)

atexit.register(clean_PID)

if 'PID_time' in data and data['PID_time'] is not None:
    sys.exit(0) 

data['PID_time'] = os.getpid()
save_settings(data)

screen_time().loop()
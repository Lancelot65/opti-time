from opti_time.block_app import block_app
from time import sleep
import json
import os
import atexit
import sys
import random

sleep(random.randint(0, 4))

def save_settings(data):
    with open('.loop.json', 'w') as fichier:
        json.dump(data, fichier, indent=4)

def load_settings():
    if not os.path.exists('.loop.json'):
        default_settings = {
            'PID_block': None
        }
        save_settings(default_settings)
        return default_settings

    with open('.loop.json', 'r') as fichier:
        return json.load(fichier)

data = load_settings()

def clean_PID():
    data['PID_block'] = None
    save_settings(data)

atexit.register(clean_PID)


if 'PID_block' in data and data['PID_block'] is not None:
    sys.exit(0)

data['PID_block'] = os.getpid()
save_settings(data)

block_app_ = block_app()
while True:
    block_app_.update()
    sleep(0.5)

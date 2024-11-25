from opti_time.block_app import block_app
from opti_time.screen_time import screen_time
from time import time, sleep

block_app_ = block_app()
screen_time_ = screen_time()
start_time = time()
while True:
    sleep(max(0, 1 - (time() - start_time)))
    screen_time_.update()
    start_time = time()
    block_app_.update()
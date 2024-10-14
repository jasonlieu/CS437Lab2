import time
from collections import deque
from time import sleep

import SpiderG
from constants import Orientation, Directions
from mapping import scan_360_to_grid, print_grid_with_path, a_star
from ultrasonic import gpio_clean_up, measure_distance

SpiderG.move_init()

SpiderG.walk(Directions.TURN_LEFT.value)
time.sleep(2)
SpiderG.servoStop()
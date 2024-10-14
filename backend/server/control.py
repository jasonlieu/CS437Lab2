import SpiderG
import time
from ultrasonic import measure_distance, gpio_clean_up
from constants import Directions

WALK_TIME = 5
TURN_TIME = 5
STOP_DISTANCE = 25

try:
    # Initial position
    SpiderG.move_init()
    while True:
        # If object detected by ultrasonic sensor, turn left
        distance = measure_distance()
        if measure_distance() < STOP_DISTANCE:
            print(f"obstacle in {distance}cm, turn left")
            SpiderG.walk(Directions.TURN_LEFT.value)
            time.sleep(TURN_TIME)

        # Else, walk forward
        else:
            print("no obstacle, forward")
            SpiderG.walk(Directions.FORWARD.value)
            time.sleep(WALK_TIME)
except KeyboardInterrupt:
    print("clean up")
    gpio_clean_up()
    SpiderG.servoStop()

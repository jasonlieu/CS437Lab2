from collections import deque
from time import sleep

import numpy as np

import SpiderG
from constants import Orientation, Directions
from mapping import scan_360_to_grid, print_grid_with_path, a_star
from ultrasonic import gpio_clean_up, measure_distance

GOAL = (19, 10)  # (0,0) - (19, 19)

MAX_DISTANCE = 300
DISTANCE_THRESHOLD = 300
TURN_TIME = 6  # Time it takes to turn 1 compass direction, fiddle with this
CARDINAL_MOVE_TIME = 5  # Time it takes to move in a cardinal direction, fiddle with this too
INTERCARDINAL_MOVE_TIME = 6  # Time it takes to move in an intercardinal direction, fiddle with this too
OBSTACLE_DISTANCE = 30  # mess with this
DEGREE_STEP = 20  # degrees per turn
GRID_SIZE = 20


class Spider:
    def __init__(self, grid_size, degree_step):
        self.grid_size = grid_size
        self.degree_step = degree_step

        # Spider starts facing south at first
        self.orientation_queue = deque(
            [Orientation.E.value, Orientation.NE.value, Orientation.N.value, Orientation.NW.value, Orientation.W.value,
             Orientation.SW.value, Orientation.S.value, Orientation.SE.value])

        self.grid = np.zeros((grid_size, grid_size))

        # Start at center
        self.current_position = (grid_size // 2, grid_size // 2)

        # Starting position
        SpiderG.move_init()

    def scan(self):
        self.grid = scan_360_to_grid(self.grid_size, degree_step=self.degree_step,
                                     distance_threshold=DISTANCE_THRESHOLD, max_distance=MAX_DISTANCE)

    def move_to(self, goal):
        print("we go to", goal)
        path = a_star(self.grid, self.current_position, goal)
        path.pop(0)
        print(path)
        print_grid_with_path(self.grid, path)

        while path and self.current_position != goal:
            try:
                next_step = path[0]

                # Turn to new orientation
                new_orientation = self.get_path_direction(next_step)
                print(self.orientation_queue[0], new_orientation)
                self.turn_to(new_orientation)

                if self.is_blocked():
                    SpiderG.servoStop()
                    # Path blocked, mark obstacle and find new path
                    self.grid[next_step[0]][next_step[1]] = 1
                    path = a_star(self.grid, self.current_position, goal)
                    if path is None:
                        print(self.grid)
                        raise Exception("No path found. Giving up")
                else:
                    # Path clear, go and remove step from path, update grid
                    self.grid[self.current_position[0]][self.current_position[1]] = 0
                    self.grid[next_step[0]][next_step[1]] = 2
                    self.current_position = next_step
                    path.pop(0)
                    self.advance(new_orientation)

                print_grid_with_path(self.grid, path)
            except Exception as e:
                print(e)
                break

    @staticmethod
    def is_blocked():
        distance = measure_distance()
        return distance <= OBSTACLE_DISTANCE

    @staticmethod
    def advance(direction):
        SpiderG.walk(Directions.FORWARD.value)
        # moving diagonally takes a bit more time
        move_time = CARDINAL_MOVE_TIME if Orientation.is_cardinal(direction) else INTERCARDINAL_MOVE_TIME
        sleep(move_time)

    def get_path_direction(self, new_position):
        coord_difference = (new_position[0] - self.current_position[0], new_position[1] - self.current_position[1])
        if coord_difference[0] > 1 or coord_difference[1] > 1:
            raise Exception(f"Next step out of reach. {self.current_position} to {new_position}")
        return coord_difference

    def turn_to(self, new_orientation):
        turns = 0
        while self.orientation_queue[0] != new_orientation:
            old_orientation = self.orientation_queue.popleft()
            self.orientation_queue.append(old_orientation)
            self.turn()
            turns += 1
            if turns == 8:
                raise Exception(f"360 turn without matching direction, check path direction. {new_orientation}")

    @staticmethod
    def turn():
        SpiderG.walk(Directions.TURN_LEFT.value)
        sleep(TURN_TIME)
        SpiderG.servoStop()

    @staticmethod
    def clean_up():
        print("clean up")
        gpio_clean_up()
        SpiderG.servoStop()
        SpiderG.move_init()


spider = Spider(GRID_SIZE, DEGREE_STEP)
try:
    spider.scan() # Optional 360 scan
    spider.move_to(GOAL)
except KeyboardInterrupt:
    spider.clean_up()
finally:
    spider.clean_up()

import time
import numpy as np
import heapq
from constants import SYMBOLS, Directions, Orientation
import SpiderG
from ultrasonic import measure_distance

DIRECTIONS = [direction.value for direction in Orientation]
TURN_TIME = 0.05

# Scan and create a 2D grid
def scan_360_to_grid(grid_size, degree_step, distance_threshold, max_distance):
    print("start scan")
    grid = np.zeros((grid_size, grid_size))
    center = grid_size // 2  # Start at center

    total_steps = 360 // degree_step  # Number of steps to complete a 360 turn

    for step in range(total_steps):
        print("step", step, "/", total_steps)
        # Measure the distance
        distance = measure_distance()
        angle = 360 - (step * degree_step) # Left turn scan

        # Calculate the position in Cartesian coordinates (relative to the center of the grid)
        if distance < max_distance:  # Only map distances within the sensor range
            x = int(center + (distance * np.cos(np.radians(angle))) / (max_distance / grid_size))
            y = int(center + (distance * np.sin(np.radians(angle))) / (max_distance / grid_size))

            # Ensure the calculated point is within the bounds of the grid
            if 0 <= x < grid_size and 0 <= y < grid_size:
                if distance < distance_threshold:
                    grid[x, y] = 1  # Obstacle
                else:
                    grid[x, y] = 0  # No obstacle

        # Rotate bot by the degree step
        SpiderG.walk(Directions.TURN_LEFT.value)
        time.sleep(TURN_TIME)

        center = grid_size // 2
        grid[center, center] = 2
        print_grid(grid)
        print("\n\n")
    return grid


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, goal):
    rows, cols = grid.shape
    open_list = []
    heapq.heappush(open_list, (0, start))  # (f_score, position)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for direction in DIRECTIONS:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:  # Within bounds
                if grid[neighbor[0], neighbor[1]] == 1:  # Obstacle
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # No path


def print_grid(grid):
    for row in grid:
        print(" ".join(SYMBOLS[cell.astype(int)] for cell in row))


def print_grid_with_path(grid, path):
    print(path)
    path_grid = grid.copy()
    for (x, y) in path:
        if path_grid[x, y] == 0:
            path_grid[x, y] = 3
    for row in path_grid:
        print(" ".join(SYMBOLS[cell.astype(int)] for cell in row))
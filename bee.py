# bee.py
from compass import Compass
import stdio

class Bee:
    def __init__(self, row, col, speed, perception):
        self.row = row
        self.col = col
        self.speed = speed
        self.perception = perception
        self.compass = Compass(row, col, speed)
        self.carrying_pollen = False

    def move(self, map_size):
        trajectory = self.compass.get_next_trajectory()
        direction = trajectory.get_direction_in_degrees()
        distance = trajectory.get_distance()

        # Calculate new position
        new_row, new_col = self.row, self.col
        if direction == 0:  # Right
            new_col += distance
        elif direction == 90:  # Up
            new_row += distance
        elif direction == 180:  # Left
            new_col -= distance
        elif direction == 270:  # Down
            new_row -= distance
        elif direction == 45:  # Up-Right
            new_row += distance
            new_col += distance
        elif direction == 135:  # Up-Left
            new_row += distance
            new_col -= distance
        elif direction == 225:  # Down-Left
            new_row -= distance
            new_col -= distance
        elif direction == 315:  # Down-Right
            new_row -= distance
            new_col += distance

        # Bound the movement by the size of the map
        self.row = max(0, min(new_row, map_size - 1))
        self.col = max(0, min(new_col, map_size - 1))

    def collect_pollen(self, flower):
        if not self.carrying_pollen and flower.has_pollen():
            flower.remove_pollen()
            self.carrying_pollen = True

    def drop_pollen(self):
        if self.carrying_pollen:
            self.carrying_pollen = False

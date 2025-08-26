# main.py
import stdio
from map import Map
from bee import Bee
from Flower import Flower

def read_map():
    # Read the first line for configuration parameters
    config_line = stdio.readString()
    n, duration, pollen_type, pollen_action = config_line.split()
    n = int(n)
    duration = int(duration)

    # Create the map
    world_map = Map(n)

    # Read the subsequent lines for flowers and hives
    line_number = 1
    while True:
        line = stdio.readString()
        if line == "":
            break  # End of input

        parts = line.split()
        if not parts:
            stdio.writeln(f"ERROR: Invalid object setup on line {line_number}")
            return

        obj_type = parts[0]
        if obj_type == 'F':
            # Flower configuration
            if len(parts) != 4:
                stdio.writeln(f"ERROR: Invalid object setup on line {line_number}")
                return
            x, y, num_pollen = map(int, parts[1:])
            flower = Flower(x, y, pollen_type)
            for _ in range(num_pollen):
                flower.add_pollen(1)  # Add pollen granules
            world_map.add_flower(flower)
        elif obj_type == 'B':
            # Bee configuration
            if len(parts) != 4:
                stdio.writeln(f"ERROR: Invalid object setup on line {line_number}")
                return
            x, y, speed, perception = map(int, parts[1:])
            bee = Bee(x, y, speed, perception)
            world_map.add_bee(bee)
        else:
            stdio.writeln(f"ERROR: Invalid object setup on line {line_number}")
            return

        line_number += 1

    return world_map

if __name__ == "__main__":
    world_map = read_map()
    if world_map:
        for _ in range(10):  # Run for 10 iterations
            world_map.update()
            world_map.print_map()

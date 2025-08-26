from handin1api import *
from compass import Compass
import stdio

def read_map():
    # Read the first line for configuration parameters
    try:
        config_line = stdio.readString()
        n, duration, pollen_type, pollen_action = config_line.split()
        n = int(n)
        duration = int(duration)
        
        # Validate pollen type and action
        if pollen_type not in ['s', 'f']:
            stdio.writeln("ERROR: Invalid configuration line")
            return
        if pollen_action not in ['max', 'min', 'sum', 'sort']:
            stdio.writeln("ERROR: Invalid configuration line")
            return
        
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
                    pollen_info = stdio.readString()
                    pollen = Pollen(pollen_info)
                    flower.add_pollen(pollen)
                world_map.add_flower(flower)
            elif obj_type in ['B', 'D', 'H', 'W']:
                # Hive configuration
                if len(parts) != 4:
                    stdio.writeln(f"ERROR: Invalid object setup on line {line_number}")
                    return
                x, y, num_entities = map(int, parts[1:])
                if obj_type == 'B':
                    hive = BeeHive(x, y, num_entities)
                    for _ in range(num_entities):
                        speed, perception = map(int, stdio.readString().split())
                        bee = Bee(x, y, speed, perception)
                        hive.add_bee(bee)
                    world_map.add_beehive(hive)
                elif obj_type == 'D':
                    hive = DesertBeeHive(x, y, num_entities)
                    for _ in range(num_entities):
                        speed, perception = map(int, stdio.readString().split())
                        bee = DesertBee(x, y, speed, perception)
                        hive.add_bee(bee)
                    world_map.add_desert_beehive(hive)
                elif obj_type == 'H':
                    hive = HoneyBeeHive(x, y, num_entities)
                    for _ in range(num_entities):
                        speed, perception = map(int, stdio.readString().split())
                        bee = HoneyBee(x, y, speed, perception)
                        hive.add_bee(bee)
                    world_map.add_honey_beehive(hive)
                elif obj_type == 'W':
                    hive = WaspHive(x, y, num_entities)
                    for _ in range(num_entities):
                        speed = int(stdio.readString())
                        wasp = Wasp(x, y, speed)
                        hive.add_wasp(wasp)
                    world_map.add_wasphive(hive)
            else:
                stdio.writeln(f"ERROR: Invalid object setup on line {line_number}")
                return
            
            line_number += 1

    except Exception as e:
        stdio.writeln("ERROR: Invalid configuration line")

def test_compass(row, col, speed, map_size, moves):
    compass = Compass(row, col, speed)
    stdio.writeln(f"{row}, {col}")
    
    for _ in range(moves):
        trajectory = compass.get_next_trajectory()
        direction = trajectory.get_direction_in_degrees()
        distance = trajectory.get_distance()
        
        # Calculate new position
        new_row = row
        new_col = col
        
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
        new_row = max(0, min(new_row, map_size - 1))
        new_col = max(0, min(new_col, map_size - 1))
        
        stdio.writeln(f"{new_row}, {new_col}")
        row, col = new_row, new_col

if __name__ == "__main__":
    # Example usage of read_map and test_compass
    read_map()
    # Uncomment the following line to test the compass function
    # test_compass(2, 3, 1, 10, 4)

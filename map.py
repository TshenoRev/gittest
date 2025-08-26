# map.py
from bee import Bee
from flower import Flower
import stdio

class Map:
    def __init__(self, size):
        self.size = size
        self.entities = []

    def add_flower(self, flower):
        self.entities.append(flower)

    def add_bee(self, bee):
        self.entities.append(bee)

    def update(self):
        for entity in self.entities:
            if isinstance(entity, Bee):
                entity.move(self.size)
                # Check for nearby flowers to collect pollen
                for flower in self.entities:
                    if isinstance(flower, Flower) and flower.row == entity.row and flower.col == entity.col:
                        entity.collect_pollen(flower)

    def print_map(self):
        stdio.writeln("Current Map:")
        for row in range(self.size):
            for col in range(self.size):
                found = False
                for entity in self.entities:
                    if entity.row == row and entity.col == col:
                        if isinstance(entity, Bee):
                            stdio.write("B ")
                        elif isinstance(entity, Flower):
                            stdio.write("F ")
                        found = True
                        break
                if not found:
                    stdio.write(". ")
            stdio.writeln()

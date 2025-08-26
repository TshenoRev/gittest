# flower.py
import stdio

class Flower:
    def __init__(self, row, col, pollen_type):
        self.row = row
        self.col = col
        self.pollen_type = pollen_type
        self.pollen_count = 0

    def add_pollen(self, pollen):
        self.pollen_count += 1

    def remove_pollen(self):
        if self.pollen_count > 0:
            self.pollen_count -= 1

    def has_pollen(self):
        return self.pollen_count > 0

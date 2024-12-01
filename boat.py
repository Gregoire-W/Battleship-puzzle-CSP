from dataclasses import dataclass


class Boat:

    id_count = 0

    def __init__(self, size):
        self.id = Boat.id_count
        Boat.id_count += 1
        self.size = size

    def __repr__(self):
        return f"Boat with id : {self.id}, size : {self.size}"
    
import numpy as np


class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x = value[0]
        self.y = value[1]


def normalize(vec):     # приведение массива к нормали
    norm = np.linalg.norm(vec)
    if norm:
        return vec / norm
    else:
        return vec

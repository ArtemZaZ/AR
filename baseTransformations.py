import numpy as np
from math import *


def getHomogeneousVector(x, y, z, w):   # Возвращает вектор в однородных координатах
    return np.array([x, y, z, w])


def getTranslationMatrix(tx, ty, tz):   # Возвращает матрицу меремещения в однородных координатах
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])


def getScalingMatrix(sx, sy, sz):       # Возвращает матрицу масштабирования в однородных координатах
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])


def getRotationMatrix(axis=None, angle=0):    # Возвращает матрицу поворота в однородных координатах
    angle = angle / 180.0 * pi
    if axis == 'x':
        return np.array([[1, 0, 0, 0],
                         [0, cos(angle), -sin(angle), 0],
                         [0, sin(angle), cos(angle), 0],
                         [0, 0, 0, 1]])
    elif axis == 'y':
        return np.array([[cos(angle), 0, sin(angle), 0],
                         [0, 1, 0, 0],
                         [-sin(angle), 0, cos(angle), 0],
                         [0, 0, 0, 1]])
    elif axis == 'z':
        return np.array([[cos(angle), -sin(angle), 0, 0],
                         [sin(angle), cos(angle), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    else:
        raise ValueError("parameter axis must be 'x', 'y', 'z' only")


if __name__ == "__main__":
    A = getTranslationMatrix(3, 5, 7)
    B = getTranslationMatrix(9, 3, 6)
    C = getScalingMatrix(1, 2, 3)
    D = getRotationMatrix('z', 45)
    vec = getHomogeneousVector(1, 2, 3, 1)
    vec2 = getHomogeneousVector(1, 0, 2, 1)
    print(A @ vec)
    print(A @ B)
    print(C @ vec)
    print(D @ vec2)


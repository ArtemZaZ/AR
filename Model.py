import numpy as np


class Mesh:
    def __init__(self, vertex=[], normals=[], faces=[], textureCoordinates=[], texture=None):
        self.__vertex = vertex
        self.__normals = normals
        self.__faces = faces
        self.__textureCoordinates = textureCoordinates
        self.__texture = texture

        self.__data = np.zeros(len(vertex), [("vertex", np.float64, 3),
                                             ("normals", np.float64, 3),
                                             ("textureCoordinates", np.float64, 2)])

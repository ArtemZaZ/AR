import numpy as np
import baseMath as bm


class Camera:
    def __init__(self):
        self.__cameraPosition = np.array([0.0, 0.0, 0.0])  # позиция камеры
        self.__cameraDirection = np.array([0.0, 0.0, 0.0])  # направление камеры
        self.__cameraRight = np.array([0.0, 0.0, 0.0])  # напрвавление правой оси камеры
        self.__cameraUp = np.array([0.0, 0.0, 0.0])  # вектор верха камеры
        self.__lookAtMatrix = np.eye(4)

    def setLookAt(self, cameraPosition, targetPosition, globalUp):
        self.__cameraPosition = np.array(cameraPosition)
        self.__cameraDirection = bm.normalize(self.__cameraPosition - targetPosition)
        self.__cameraRight = bm.normalize(np.cross(globalUp, self.__cameraDirection))
        self.__cameraUp = np.cross(self.__cameraDirection, self.__cameraRight)

        firstPart = np.eye(4)
        firstPart[0:3, 0:3] = [self.__cameraRight, self.__cameraUp, self.__cameraDirection]
        secondPart = np.eye(4)
        secondPart[:, 0:3] = self.__cameraPosition
        return firstPart @ secondPart

    @property
    def LookAtMatrix(self):
        return self.__lookAtMatrix

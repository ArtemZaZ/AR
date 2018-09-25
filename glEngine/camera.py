import numpy as np
from glEngine.base import baseMath as bm


class Camera:
    def __init__(self):
        self._cameraPosition = np.array([0.0, 0.0, 0.0])  # позиция камеры
        self._cameraDirection = np.array([0.0, 0.0, 0.0])  # направление камеры
        self._cameraRight = np.array([0.0, 0.0, 0.0])  # напрвавление правой оси камеры
        self._cameraUp = np.array([0.0, 0.0, 0.0])  # вектор верха камеры
        self._lookAtMatrix = np.eye(4)

    def setLookAt(self, cameraPosition, targetPosition, globalUp):
        self._cameraPosition = np.array(cameraPosition)
        self._cameraDirection = bm.normalize(self._cameraPosition - targetPosition)
        self._cameraRight = bm.normalize(np.cross(globalUp, self._cameraDirection))
        self._cameraUp = np.cross(self._cameraDirection, self._cameraRight)

        firstPart = np.eye(4)
        firstPart[0:3, 0:3] = [self._cameraRight, self._cameraUp, self._cameraDirection]
        secondPart = np.eye(4)
        secondPart[:, 0:3] = self._cameraPosition
        return firstPart @ secondPart

    @property
    def lookAtMatrix(self):
        return self._lookAtMatrix

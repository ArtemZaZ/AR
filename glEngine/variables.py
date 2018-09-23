from glEngine.glObject import GLObject
import OpenGL.GL as gl
import numpy as np
from glEngine.types import *


class Variable(GLObject):
    def __init__(self, name, program, type, data):
        if type not in variableTypes:
            raise TypeError("Unknown variable type")
        GLObject.__init__(self)
        self._program = program
        self._name = name
        self._type = type
        self._data = data
        self._location = None
        """ Вспомогательные переменные, для обновления данных формы """
        self._isMat = None
        self._updateFunction = None
        self._count = None

    @property
    def name(self):
        return self._name

    @property
    def program(self):
        return self._program

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class Uniform(Variable):
    def __init__(self, *args, **kwargs):
        Variable.__init__(self, *args, **kwargs)

    def _create(self):
        gl.glUseProgram(self._program)
        self._location = gl.glGetUniformLocation(self._program, self._name)
        self._updateFunction, self._count, self._isMat = uniformTypesToFunctions[self._type]
        if self._isMat:
            self._updateFunction(self._location, self._count, False, self._data)
        else:
            self._updateFunction(self._location, self._count, self._data)
        gl.glUseProgram(0)

    def _update(self):
        # TODO: Переделать под одну статичную ф-ию
        if self._isMat:
            self._updateFunction(self._location, self._count, False, self._data)
        else:
            self._updateFunction(self._location, self._count, self._data)


if __name__ == "__main__":
    pass

from glEngine.glObject import GLObject
import OpenGL.GL as gl
import numpy as np

# TODO: в процессе дополнить
_variableTypes = [gl.GL_FLOAT, gl.GL_DOUBLE, gl.GL_BYTE,
                  gl.GL_UNSIGNED_BYTE, gl.GL_SHORT,
                  gl.GL_UNSIGNED_SHORT, gl.GL_UNSIGNED_INT,
                  gl.GL_UNSIGNED_INT64, gl.GL_CHAR,
                  gl.GL_INT, gl.GL_BOOL,
                  gl.GL_HALF_NV, gl.GL_VOID_P,
                  gl.GL_FLOAT_VEC2, gl.GL_FLOAT_VEC3,
                  gl.GL_FLOAT_VEC4,
                  gl.GL_FLOAT_MAT2, gl.GL_FLOAT_MAT3,
                  gl.GL_FLOAT_MAT4,
                  gl.GL_SAMPLER_1D, gl.GL_SAMPLER_2D,
                  gl.GL_SAMPLER_CUBE]

# TODO: в процессе дополнить
_variableTypesInfo = {
    gl.GL_FLOAT: np.float32,
    gl.GL_DOUBLE: np.float64,
    gl.GL_INT: np.int32,
    gl.GL_UNSIGNED_INT: np.uint32
}


class Variable(GLObject):
    def __init__(self, name, program, type, data):
        if type not in _variableTypes:
            raise TypeError("Unknown variable type")
        GLObject.__init__(self)
        self._program = program
        self._name = name
        self._type = type
        self._data = data
        self._location = None

    @property
    def name(self):
        return self._name

    @property
    def program(self):
        return self._program

    @property
    def data(self):
        return self._data


class Attribute(Variable):
    def __init__(self, *args, **kwargs):
        Variable.__init__(self, *args, **kwargs)

    def _create(self):
        self._location = gl.glGetAttribLocation(self._program, self._name)

    def setVertexAttribPointer(self, stride, offset):
        gl.glEnableVertexAttribArray(self._location)
        gl.glVertexAttribPointer(self._location, self._data.shape[1], self._type, False, stride, offset)

    @property
    def numpyInfoTurple(self):
        return self._name, _variableTypesInfo.get(type), self._data.shape[1]


class Uniform(Variable):
    def __init__(self, *args, **kwargs):
        Variable.__init__(self, *args, **kwargs)


if __name__ == "__main__":
    a = Attribute(name="position", program=1, type=gl.GL_DOUBLE, data=None)

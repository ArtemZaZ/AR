from glEngine.glObject import GLObject
import OpenGL.GL as gl
import numpy as np
import ctypes

_buffersTypes = [gl.GL_ELEMENT_ARRAY_BUFFER, gl.GL_ARRAY_BUFFER]

_variable_G_to_N = {
    gl.GL_FLOAT: np.float32,
    gl.GL_DOUBLE: np.float64,
    gl.GL_INT: np.int32,
    gl.GL_UNSIGNED_INT: np.uint32
}

_variable_N_to_G = {
    np.dtype(np.float32): gl.GL_FLOAT,
    np.dtype(np.float64): gl.GL_DOUBLE,
    np.dtype(np.int32): gl.GL_INT,
    np.dtype(np.uint32): gl.GL_UNSIGNED_INT
}


class GPUBuffer(GLObject, np.ndarray):
    def __new__(cls, *args, type=None, **kwargs):
        if type not in _buffersTypes:
            raise TypeError("Unknown buffer type")
        cls._type = type
        return np.ndarray.__new__(cls, *args, **kwargs)

    def __init__(self, *args, type=None, **kwargs):
        if type not in _buffersTypes:
            raise TypeError("Unknown buffer type")

        GLObject.__init__(self)
        self._type = type

    def _create(self):
        if self._type is not None:  # если тип не None(glVertexArray or Index)
            self._descriptor = gl.glGenBuffers(1)
        else:
            raise TypeError("None buffer type")

    def bind(self):
        if self._descriptor and (self._type in _buffersTypes):
            gl.glBindBuffer(self._type, self._descriptor)

    def unbind(self):
        gl.glBindBuffer(self._type, 0)


class VertexBuffer(GPUBuffer):
    def __new__(cls, program, *args, **kwargs):
        #cls._attribPropertyDict = {}
        cls._program = program
        return GPUBuffer.__new__(cls, *args, type=gl.GL_ARRAY_BUFFER, **kwargs)

    def __init__(self, program, *args, **kwargs):
        self._program = program
        GPUBuffer.__init__(self, *args, type=gl.GL_ARRAY_BUFFER, **kwargs)

    def _create(self):
        GPUBuffer._create(self)
        if self.dtype.fields:
            offsetD = 0
            for key in self.dtype.fields.keys():
                offset = ctypes.c_void_p(offsetD)
                location = gl.glGetAttribLocation(self._program, key)
                gl.glEnableVertexAttribArray(location)
                gl.glBindBuffer(self._type, self._descriptor)
                gl.glVertexAttribPointer(location, self[key].shape[1], _variable_N_to_G[self[key].dtype], False,
                                         self.strides[0], offset)
                offsetD += self.dtype[key].itemsize
            gl.glBufferData(self._type, self.nbytes, self, gl.GL_DYNAMIC_DRAW)
            gl.glBindBuffer(self._type, 0)

    def _update(self):
        self.bind()
        gl.glBufferData(self._type, self.nbytes, self, gl.GL_DYNAMIC_DRAW)
        self.unbind()



if __name__ == "__main__":
    data = np.zeros(3, [("position", np.float64, 3)]).view(GPUBuffer)
    data.__init__(type=gl.GL_ELEMENT_ARRAY_BUFFER)
    data2 = GPUBuffer(type=gl.GL_ARRAY_BUFFER, shape=(2,), buffer=np.array([1, 2, 3]), offset=np.int_().itemsize,
                      dtype=int)

    # data.create()
    # data2.create()

from glEngine.glObject import GLObject
import OpenGL.GL as gl
import numpy as np

_buffersTypes = [gl.GL_ELEMENT_ARRAY_BUFFER, gl.GL_ARRAY_BUFFER]


class GPUBuffer(GLObject, np.ndarray):
    def __new__(cls, *args, **kwargs):
        if cls._type not in _buffersTypes:
            raise TypeError("Unknown buffer type")

        return np.ndarray.__new__(cls, *args, **kwargs)

    def __init__(self, type, count, *args, **kwargs):
        if type not in _buffersTypes:
            raise TypeError("Unknown buffer type")

        GLObject.__init__(self)
        self._type = type
        self._count = count

    def _create(self):
        if self._type is not None:  # если тип не None(glVertexArray or Index)
            self._descriptor = gl.glGenBuffers(1)
        else:
            raise TypeError("None buffer type")


class VertexBuffer(GPUBuffer):
    def __init__(self, *args, **kwargs):
        self._attribList = kwargs.get("attribList")
        if self._attribList:
            nlist = []
            for attribute in self._attribList:
                nlist.append(attribute.numpyInfoTurple)
        else:
            GPUBuffer.__init__(type=gl.GL_ARRAY_BUFFER, *args, **kwargs)



if __name__ == "__main__":
    data = np.zeros(3, [("position", np.float64, 3)]).view(GPUBuffer)
    data.__init__(type=gl.GL_ELEMENT_ARRAY_BUFFER)
    data2 = GPUBuffer(type=gl.GL_ARRAY_BUFFER, shape=(2,), buffer=np.array([1, 2, 3]), offset=np.int_().itemsize, dtype=int)
    print(data)
    print(data2)

    data.create()
    data2.create()

    # print(data)
    # print(type(data))

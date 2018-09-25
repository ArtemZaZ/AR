from glEngine.glObject import GLObject
import OpenGL.GL as gl
import numpy as np
import ctypes
from glEngine.types import *
import warnings

""" Допустимые типы для GPUBuffer"""
_buffersTypes = [gl.GL_ELEMENT_ARRAY_BUFFER, gl.GL_ARRAY_BUFFER]


class GPUBuffer(GLObject, np.ndarray):
    """
    Базовый класс буффера видеокарты
    """
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

    def _bind(self):
        if self._descriptor and (self._type in _buffersTypes):
            gl.glBindBuffer(self._type, self._descriptor)

    def _unbind(self):
        gl.glBindBuffer(self._type, 0)


class VertexBuffer(GPUBuffer):
    """
    Класс OpenGL VBO
    """
    def __new__(cls, program, *args, **kwargs):
        #cls._attribPropertyDict = {}
        cls._program = program
        return GPUBuffer.__new__(cls, *args, type=gl.GL_ARRAY_BUFFER, **kwargs)

    def __init__(self, program, *args, **kwargs):
        self._program = program
        GPUBuffer.__init__(self, *args, type=gl.GL_ARRAY_BUFFER, **kwargs)

    def _create(self):
        GPUBuffer._create(self)     # создаем буффер
        if self.dtype.fields:   # если есть аттрибуты
            offsetD = 0
            for key in self.dtype.fields.keys():    # проходимся по каждому аттрибуту
                offset = ctypes.c_void_p(offsetD)   # смещение данных в буффере
                location = gl.glGetAttribLocation(self._program, key)   # ищем необходимый нам аттрибут
                gl.glEnableVertexAttribArray(location)  # включаем его
                self.bind()
                gl.glVertexAttribPointer(location, self[key].shape[1], variable_N_to_G[self[key].dtype], False,
                                         self.strides[0], offset)   # указываем, как будут идти данные
                offsetD += self.dtype[key].itemsize     # добавляем смещение
            gl.glBufferData(self._type, self.nbytes, self.data, gl.GL_DYNAMIC_DRAW)      # загружаем данные в видеопамять
            self.unbind()

    def _update(self):
        self.bind()
        gl.glBufferData(self._type, self.nbytes, self, gl.GL_DYNAMIC_DRAW)
        self.unbind()


class IndexBuffer(GPUBuffer):
    """
    OpenGL IBO/EBO
    """
    def __new__(cls, *args, **kwargs):
        return GPUBuffer.__new__(cls, *args, type=gl.GL_ELEMENT_ARRAY_BUFFER, **kwargs)

    def __init__(self, *args, **kwargs):
        GPUBuffer.__init__(self, *args, type=gl.GL_ELEMENT_ARRAY_BUFFER, **kwargs)

    def _create(self):
        GPUBuffer._create(self)
        self._update()

    def _update(self):
        self.bind()
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.nbytes, self.data, gl.GL_DYNAMIC_DRAW)
        self.unbind()


if __name__ == "__main__":
    data = np.zeros(3, [("position", np.float64, 3)]).view(GPUBuffer)
    data.__init__(type=gl.GL_ELEMENT_ARRAY_BUFFER)
    data2 = GPUBuffer(type=gl.GL_ARRAY_BUFFER, shape=(2,), buffer=np.array([1, 2, 3]), offset=np.int_().itemsize,
                      dtype=int)

    # data.create()
    # data2.create()

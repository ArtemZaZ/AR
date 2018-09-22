import OpenGL.GL as gl
from glEngine.glObject import GLObject
from glEngine.buffers import *
import numpy as np


class VertexArray(GLObject):
    def __init__(self):
        GLObject.__init__(self)
        self._vbo = None
        self._ibo = None

    def _create(self):
        self._descriptor = gl.glGenVertexArrays(1)
        self.bind()
        self._vbo.create()
        self._ibo.create()
        self.unbind()

    @property
    def vbo(self):
        return self._vbo

    @vbo.setter
    def vbo(self, vbo):
        if type(vbo) is not VertexBuffer:
            raise TypeError("VBO must be VertexBuffer")
        self._vbo = vbo

    @property
    def ibo(self):
        return self._ibo

    @ibo.setter
    def ibo(self, ibo):
        if type(ibo) is not IndexBuffer:
            raise TypeError("IBO must be IndexBuffer")
        self._ibo = ibo

    def _bind(self):
        gl.glBindVertexArray(self._descriptor)

    def _unbind(self):
        gl.glBindVertexArray(0)

    def draw(self, mode=gl.GL_TRIANGLE_STRIP):
        self.bind()
        self._ibo.bind()
        #gl.glDrawArrays(mode, self._descriptor, self._vbo.size)
        gl.glDrawElements(mode, self._ibo.size, gl.GL_UNSIGNED_INT, None)
        self._ibo.unbind()
        self.unbind()

import OpenGL.GL as gl
from OpenGL.GL import shaders
import baseMath as bm
import numpy as np
import baseShaders as bs
import ctypes


class Sprite:
    def __init__(self, rectangle=None, textureRegion=None,
                 vertexShaderSource=bs.baseSpriteVertexShader,
                 fragmentShaderSource=bs.baseSpriteFragmentShader):
        self.__rectangle = rectangle
        self.__textureRegion = textureRegion
        self.__program = shaders.compileProgram(
            shaders.compileShader(vertexShaderSource, gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragmentShaderSource, gl.GL_FRAGMENT_SHADER)
        )
        self.__data = np.zeros(4, [("vertex", np.float32, 2),
                                   ("textureCoordinates", np.float32, 2)])

        self.__vboDataBuffer = gl.glGenBuffers(1)
        self.__vaoDataBuffer = gl.glGenVertexArrays(1)
        stride = self.__data.strides[0]

        gl.glBindVertexArray(self.__vaoDataBuffer)

        offset = ctypes.c_void_p(0)
        self.__vertexLocation = gl.glGetAttribLocation(self.__program, "vertex")
        gl.glEnableVertexAttribArray(self.__vertexLocation)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__vboDataBuffer)
        gl.glVertexAttribPointer(self.__vertexLocation, 2, gl.GL_FLOAT, False, stride, offset)

        offset = ctypes.c_void_p(self.__data.dtype["vertex"].itemsize)
        self.__textureCoordinatesLocation = gl.glGetAttribLocation(self.__program, "textureCoordinates")
        gl.glEnableVertexAttribArray(self.__textureCoordinatesLocation)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__vboDataBuffer)
        gl.glVertexAttribPointer(self.__textureCoordinatesLocation, 2, gl.GL_FLOAT, False, stride, offset)

        r = self.__rectangle
        tr = self.__textureRegion
        self.__data["vertex"][...] = (r.x, r.y), (r.x + r.width, r.y),\
                                     (r.x, r.y - r.height), (r.x + r.width, r.y - r.height)

        self.__data["textureCoordinates"][...] = (tr.x, tr.y), (tr.x + tr.width, tr.y), \
                                                 (tr.x, tr.y - tr.height), (tr.x + tr.width, tr.y - tr.height)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.__data.nbytes, self.__data, gl.GL_DYNAMIC_DRAW)
        gl.glBindVertexArray(0)

    def updateAttributes(self):
        gl.glBindVertexArray(self.__vaoDataBuffer)
        r = self.__rectangle
        tr = self.__textureRegion
        self.__data["vertex"][...] = (r.x, r.y), (r.x + r.width, r.y), \
                                     (r.x, r.y - r.height), (r.x + r.width, r.y - r.height)

        self.__data["textureCoordinates"][...] = (tr.x, tr.y), (tr.x + tr.width, tr.y), \
                                                 (tr.x, tr.y - tr.height), (tr.x + tr.width, tr.y - tr.height)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.__data.nbytes, self.__data, gl.GL_DYNAMIC_DRAW)
        gl.glBindVertexArray(0)

    @property
    def rectangle(self):
        """
        Через свойство можно изменить параметры объекта, т.к. возвращается ссылка на него
        :return:
        """
        return self.__rectangle

    @rectangle.setter
    def rectangle(self, rectangle):
        self.__rectangle = rectangle

    @property
    def textureRegion(self):
        return self.__textureRegion

    @textureRegion.setter
    def textureRegion(self, textureRegion):
        self.__textureRegion = textureRegion

    def draw(self):
        gl.glUseProgram(self.__program)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textureRegion.texture)
        gl.glBindVertexArray(self.__vaoDataBuffer)
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.__data.shape[0])
        gl.glBindVertexArray(0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glUseProgram(0)



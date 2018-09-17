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
        self.rectangle = rectangle
        self.textureRegion = textureRegion
        self.__program = shaders.compileProgram(
            shaders.compileShader(vertexShaderSource, gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragmentShaderSource, gl.GL_FRAGMENT_SHADER)
        )
        self.__data = np.zeros(4, [("vertex", np.float32, 2),
                                   ("textureCoordinates", np.float32, 2)])

        self.__gpuDataBuffer = gl.glGenBuffers(1)
        stride = self.__data.strides[0]

        offset = ctypes.c_void_p(0)
        self.__vertexLocation = gl.glGetAttribLocation(self.__program, "vertex")
        gl.glEnableVertexAttribArray(self.__vertexLocation)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__gpuDataBuffer)
        gl.glVertexAttribPointer(self.__vertexLocation, 2, gl.GL_FLOAT, False, stride, offset)

        offset = ctypes.c_void_p(self.__data.dtype["vertex"].itemsize)
        self.__textureCoordinatesLocation = gl.glGetAttribLocation(self.__program, "textureCoordinates")
        gl.glEnableVertexAttribArray(self.__textureCoordinatesLocation)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__gpuDataBuffer)
        gl.glVertexAttribPointer(self.__textureCoordinatesLocation, 2, gl.GL_FLOAT, False, stride, offset)

        r = self.rectangle
        tr = self.textureRegion
        self.__data["vertex"][...] = (r.x, r.y), (r.x, r.y + r.width),\
                                     (r.x - r.height, r.y + r.width), (r.x - r.height, r.y)

        self.__data["textureCoordinates"][...] = (tr.x, tr.y), (tr.x, tr.y + tr.width),\
                                                 (tr.x - tr.height, tr.y + tr.width), (tr.x - tr.height, tr.y)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.__data.nbytes, self.__data, gl.GL_DYNAMIC_DRAW)

    def draw(self):
        gl.glUseProgram(self.__program)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__gpuDataBuffer)
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.__data.shape[0])
        gl.glUseProgram(0)



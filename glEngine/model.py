import numpy as np
import OpenGL.GL as gl
from OpenGL.GL import shaders
from glEngine.arrays import VertexArray
from glEngine.buffers import VertexBuffer, IndexBuffer


class Mesh:
    def __init__(self, vertexShader=None, fragmentShader=None, vertices=None, normals=None, faces=None, textureCoordinates=None, texture=None):
        self._vertexShaderSource = vertexShader
        self._fragmentShaderSource = fragmentShader
        self._vertices = vertices
        self._normals = normals
        self._faces = faces
        self._textureCoordinates = textureCoordinates
        self._texture = texture
        self._vao = None
        self._vertexBuffer = None
        self._indexBuffer = None

        self._program = shaders.compileProgram(
            shaders.compileShader(self._vertexShaderSource, gl.GL_VERTEX_SHADER),
            shaders.compileShader(self._fragmentShaderSource, gl.GL_FRAGMENT_SHADER)
        )

    def create(self):
        gl.glUseProgram(self._program)
        self._vao = VertexArray()
        self._vertexBuffer = np.zeros(self._vertices.shape[0], [("position", np.float64, 3)]).view(VertexBuffer)
        self._vertexBuffer.__init__(self._program)
        self._vertexBuffer["position"][...] = self._vertices
        self._indexBuffer = np.zeros(self._faces.shape, dtype=np.uint32).view(IndexBuffer)
        self._indexBuffer.__init__()
        self._indexBuffer[...] = self._faces
        self._vao.vbo = self._vertexBuffer
        self._vao.ibo = self._indexBuffer
        self._vao.create()
        gl.glUseProgram(0)

    @property
    def program(self):
        return self._program

    def draw(self, mode=gl.GL_TRIANGLE_STRIP):
        gl.glUseProgram(self._program)
        self._vao.draw(mode=mode)
        gl.glUseProgram(0)


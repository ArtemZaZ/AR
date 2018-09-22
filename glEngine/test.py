import glfw
import OpenGL.GL as gl
import glEngine.buffers
import sys
from OpenGL.GL import shaders
import glEngine.TestClass as Test
import numpy as np
from glEngine.buffers import VertexBuffer, IndexBuffer
from glEngine.arrays import VertexArray

test = Test.Test()


def init(self):
    gl.glUseProgram(self.program)
    self.vao = VertexArray()
    self.vertexBuffer = np.zeros(8, [("position", np.float32, 3),
                                     ("color", np.float32, 4)]).view(VertexBuffer)

    self.vertexBuffer["position"] = [[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                                     [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]]
    self.vertexBuffer["color"] = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
                                  [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]]
    self.vertexBuffer.__init__(self.program)
    self.indexBuffer = np.array([0, 1, 1, 2, 2, 3, 3, 0,
                                 4, 7, 7, 6, 6, 5, 5, 4,
                                 0, 5, 1, 6, 2, 7, 3, 4], dtype=np.uint32).view(IndexBuffer)
    self.indexBuffer.__init__()
    self.vao.vbo = self.vertexBuffer
    self.vao.ibo = self.indexBuffer
    self.vao.create()
    gl.glEnable(gl.GL_DEPTH_TEST)


def run(self):
    self.vao.draw(mode=gl.GL_TRIANGLE_STRIP)

test.initFunc = init
test.runFunc = run

test.run()

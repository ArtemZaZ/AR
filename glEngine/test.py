import glfw
import OpenGL.GL as gl
import glEngine.buffers
import sys
from OpenGL.GL import shaders
import glEngine.TestClass as Test
import numpy as np
from glEngine.buffers import VertexBuffer


test = Test.Test()


def init(self):
    gl.glUseProgram(self.program)
    self.vertexBuffer = np.zeros(3, [("position", np.float64, 3), ("color", np.float64, 4)]).view(VertexBuffer)
    self.vertexBuffer.__init__(self.program)
    self.vertexBuffer.create()
    self.vertexBuffer["position"][...] = (-1, -1, 0), (0, 1, 0), (0, 0, 0)
    self.vertexBuffer["color"][...] = (0, 1, 0, 1), (1, 0, 0, 1), (0, 0, 1, 1)
    self.vertexBuffer.update()


def run(self):
    self.vertexBuffer.bind()
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, self.vertexBuffer.shape[0])
    self.vertexBuffer.unbind()


test.initFunc = init
test.runFunc = run

test.run()







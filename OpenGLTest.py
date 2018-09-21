import sys
import glfw
import OpenGL.GL as gl
import numpy as np
import ctypes
from OpenGL.GL import shaders
import baseTransformations as bt
import time
import Texture
import gloo
import trimesh


# http://www.labri.fr/perso/nrougier/python-opengl/


def loadShaderSourceFromFile(fileName):
    file = open(fileName, 'r')
    return file.read()


if not glfw.init():
    sys.exit()

WIDTH = 800
HEIGHT = 600
window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)

program = shaders.compileProgram(
    shaders.compileShader(loadShaderSourceFromFile("vertexShader.shader"), gl.GL_VERTEX_SHADER),
    shaders.compileShader(loadShaderSourceFromFile("fragmentShader.shader"), gl.GL_FRAGMENT_SHADER)
)

gl.glUseProgram(program)

Texture.loadTexture("images/testImage.png")

mesh = trimesh.load('models/tube.obj')

# data = np.zeros((4, 3), dtype=np.float32)
data = np.zeros(6, [("position", np.float64, 3),
                    ("color", np.float64, 4),
                    ("texture_coord", np.float64, 2)])
data['position'] = [[0, 0, 1], [1, 0, -1], [-1, 0, -1], [0, 1, 0],
                    [0, 0, 1], [1, 0, -1]]
data['color'] = (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), (0, 0, 1, 1), \
                (0.5, 1, 0, 1), (1, 0.5, 0, 1)

data['texture_coord'] = [[0, 0], [0, 1], [1, 1], [0, 0], [0, 1], [1, 1]]
buffer = gl.glGenBuffers(1)
stride = data.strides[0]
print(stride)
offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 3, gl.GL_DOUBLE, False, stride, offset)

"""
offset = ctypes.c_void_p(data.dtype["position"].itemsize)
loc = gl.glGetAttribLocation(program, "color")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 4, gl.GL_DOUBLE, False, stride, offset)
"""

offset = ctypes.c_void_p(data.dtype["position"].itemsize + data.dtype["color"].itemsize)
loc = gl.glGetAttribLocation(program, "textCoord")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 2, gl.GL_DOUBLE, False, stride, offset)

perspective = gl.glGetUniformLocation(program, "perspective")
view = gl.glGetUniformLocation(program, "view")
model = gl.glGetUniformLocation(program, "model")
eye = np.eye(4)

gl.glUniformMatrix4fv(perspective, 1, False, eye)
gl.glUniformMatrix4fv(view, 1, False, eye)
gl.glUniformMatrix4fv(model, 1, False, eye)

# Upload CPU data to GPU buffer
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

translationMatrix = bt.getTranslationMatrix(0, 0, -2)
gl.glUniformMatrix4fv(view, 1, False, translationMatrix.transpose())

perspectiveMatrix = bt.getPerspectiveMatrix(90, 100, 1, WIDTH / (2 * HEIGHT))
gl.glUniformMatrix4fv(perspective, 1, False, perspectiveMatrix.transpose())

angle = 0.0
vec = [0.5, 0.5, 1, 1]

print(perspectiveMatrix @ translationMatrix @ eye @ vec)

while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    # translate = bt.getTranslationMatrix(0, 0, 1.0)
    matrix = bt.getRotationMatrix('z', angle)
    matrix2 = bt.getRotationMatrix('x', angle * 2)
    gl.glUniformMatrix4fv(model, 1, False, matrix2 @ matrix)
    gl.glViewport(0, 0, 400, 600)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, data.shape[0])
    gl.glViewport(400, 0, 400, 600)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, data.shape[0])
    glfw.swap_buffers(window)
    time.sleep(0.01)
    angle += 0.4

glfw.terminate()

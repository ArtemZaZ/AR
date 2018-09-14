import sys
import glfw
import OpenGL.GL as gl
import numpy as np
import ctypes
from OpenGL.GL import shaders
import baseTransformations as bt
import time

# http://www.labri.fr/perso/nrougier/python-opengl/


def loadShaderSourceFromFile(fileName):
    file = open(fileName, 'r')
    return file.read()


if not glfw.init():
    sys.exit()

window = glfw.create_window(800, 600, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)

program = shaders.compileProgram(
    shaders.compileShader(loadShaderSourceFromFile("vertexShader.shader"), gl.GL_VERTEX_SHADER),
    shaders.compileShader(loadShaderSourceFromFile("fragmentShader.shader"), gl.GL_FRAGMENT_SHADER)
)


gl.glUseProgram(program)

data = np.zeros((4, 3), dtype=np.float32)
buffer = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
stride = data.strides[0]

offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)
# Assign CPU data
data[...] = (-0.5, -0.5, 2.0), (-0.5, 0.5, 2.0), (0.5, -0.5, 2.0), (0.5, 0.5, 2.0)

color = gl.glGetUniformLocation(program, "color")
perspective = gl.glGetUniformLocation(program, "perspective")
view = gl.glGetUniformLocation(program, "view")
model = gl.glGetUniformLocation(program, "model")
eye = np.eye(4)

gl.glUniform4f(color, 0.0, 0.0, 1.0, 1.0)
gl.glUniformMatrix4fv(perspective, 1, False, eye)
gl.glUniformMatrix4fv(view, 1, False, eye)
gl.glUniformMatrix4fv(model, 1, False, eye)

# Upload CPU data to GPU buffer
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

translationMatrix = bt.getTranslationMatrix(0, 0, -2)
gl.glUniformMatrix4fv(view, 1, False, translationMatrix.transpose())

perspectiveMatrix = bt.getPerspectiveMatrix(90, 100, 1, 1)
gl.glUniformMatrix4fv(perspective, 1, False, perspectiveMatrix.transpose())


vec = (-0.5, -0.5, 2.0, 1.0)
print(perspectiveMatrix @ eye @ translationMatrix @ vec)

angle = 0.0

while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    #translate = bt.getTranslationMatrix(0, 0, 1.0)
    matrix = bt.getRotationMatrix('z', angle)
    gl.glUniformMatrix4fv(model, 1, False, matrix)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, data.shape[0])
    glfw.swap_buffers(window)
    time.sleep(0.01)
    angle += 0.2


glfw.terminate()

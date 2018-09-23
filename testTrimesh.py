import trimesh
import OpenGL.GL as gl
import ctypes
from OpenGL.GL import shaders
import numpy as np
import sys
import glfw
import baseTransformations as bt
import time

if not glfw.init():
    sys.exit()

WIDTH = 800
HEIGHT = 600
window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)

def loadShaderSourceFromFile(fileName):
    file = open(fileName, 'r')
    return file.read()


program = shaders.compileProgram(
    shaders.compileShader(loadShaderSourceFromFile("vertexShader.shader"), gl.GL_VERTEX_SHADER),
    shaders.compileShader(loadShaderSourceFromFile("fragmentShader.shader"), gl.GL_FRAGMENT_SHADER)
)

mesh = trimesh.load('models/tube.obj')



print(type(mesh.vertices))
print(type(mesh.metadata['vertex_texture']))

data = np.zeros(mesh.vertices.shape[0], [("position", np.dtype(np.float64), 3)])
faces = np.zeros(mesh.faces.shape, dtype=np.uint32)
faces[...] = mesh.faces
print(faces)

data["position"] = mesh.vertices

gl.glUseProgram(program)
buffer = gl.glGenBuffers(1)
EBO = gl.glGenBuffers(1)


stride = data.strides[0]
print(stride)
offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 3, gl.GL_DOUBLE, False, stride, offset)

perspective = gl.glGetUniformLocation(program, "perspective")
view = gl.glGetUniformLocation(program, "view")
model = gl.glGetUniformLocation(program, "model")
eye = np.eye(4)

gl.glUniformMatrix4fv(perspective, 1, False, eye)
gl.glUniformMatrix4fv(view, 1, False, eye)
gl.glUniformMatrix4fv(model, 1, False, eye)

# Upload CPU data to GPU buffer
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data.transpose(), gl.GL_DYNAMIC_DRAW)

translationMatrix = bt.getTranslationMatrix(0, 0, -2)
gl.glUniformMatrix4fv(view, 1, False, translationMatrix.transpose())

perspectiveMatrix = bt.getPerspectiveMatrix(90, 100, 1, WIDTH / (2 * HEIGHT))
gl.glUniformMatrix4fv(perspective, 1, False, perspectiveMatrix.transpose())
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, gl.GL_DYNAMIC_DRAW)

angle = 0.0

while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    # translate = bt.getTranslationMatrix(0, 0, 1.0)
    matrix = bt.getRotationMatrix('z', angle)
    matrix2 = bt.getRotationMatrix('x', angle * 2)
    gl.glUniformMatrix4fv(model, 1, False, matrix2 @ matrix)
    gl.glViewport(0, 0, 400, 600)
    gl.glDrawElements(gl.GL_TRIANGLES, faces.size, gl.GL_UNSIGNED_INT, None)
    gl.glViewport(400, 0, 400, 600)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, data.shape[0])
    glfw.swap_buffers(window)
    time.sleep(0.01)
    angle += 0.4

glfw.terminate()
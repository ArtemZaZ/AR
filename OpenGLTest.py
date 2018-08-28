import sys
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import numpy as np
import ctypes
from OpenGL.GL import shaders

# http://www.labri.fr/perso/nrougier/python-opengl/


def loadShaderSourceFromFile(fileName):
    file = open(fileName, 'r')
    return file.read()


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
    glut.glutSwapBuffers()


def reshape(width, height):
    gl.glViewport(0, 0, width, height)


def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()


glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow('OpenGL Test')
glut.glutReshapeWindow(512, 512)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

program = shaders.compileProgram(
    shaders.compileShader(loadShaderSourceFromFile("vertexShader.shader"), gl.GL_VERTEX_SHADER),
    shaders.compileShader(loadShaderSourceFromFile("fragmentShader.shader"), gl.GL_FRAGMENT_SHADER)
)

gl.glUseProgram(program)

data = np.zeros((4, 2), dtype=np.float32)
buffer = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
stride = data.strides[0]

offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)
# Assign CPU data
data[...] = (-1, +1), (+1, +1), (-0, -1), (+1, -0.5)

# Upload CPU data to GPU buffer
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

glut.glutMainLoop()

import glfw
import OpenGL.GL as gl
import glEngine.buffers
import sys
from OpenGL.GL import shaders
import trimesh
import time
import numpy as np
import baseTransformations as bt
WIDTH = 800
HEIGHT = 600

vertexShader = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;
attribute vec3 position;
attribute vec4 color;
varying vec4 vColor;

void main(void)
{
    vColor = color;
    gl_Position = perspective * view * model * vec4(position, 1.0);
}

"""

fragmentShader = """
varying vec4 vColor;
void main()
{
    gl_FragColor = vColor;
}
"""


class Test:
    def __init__(self, initFunc, runFunc):
        if not glfw.init():
            sys.exit()

        self.initFunc = initFunc
        self.runFunc = runFunc

        self.window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

        if not self.window:
            glfw.terminate()
            sys.exit()

        glfw.make_context_current(self.window)
        self.initFunc(self)

        gl.glUseProgram(self.mesh.program)
        self.perspective = gl.glGetUniformLocation(self.mesh.program, "perspective")
        self.view = gl.glGetUniformLocation(self.mesh.program, "view")
        self.model = gl.glGetUniformLocation(self.mesh.program, "model")
        self.eye = np.eye(4)

        gl.glUniformMatrix4fv(self.perspective, 1, False, self.eye)
        gl.glUniformMatrix4fv(self.view, 1, False, self.eye)
        gl.glUniformMatrix4fv(self.model, 1, False, self.eye)

        translationMatrix = bt.getTranslationMatrix(0, 0, -300)
        gl.glUniformMatrix4fv(self.view, 1, False, translationMatrix.transpose())

        perspectiveMatrix = bt.getPerspectiveMatrix(90, 1000, 1, WIDTH / HEIGHT)
        gl.glUniformMatrix4fv(self.perspective, 1, False, perspectiveMatrix.transpose())
        self.angle = 0.0
        gl.glUseProgram(0)

    def initFunc(self):
        pass

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glUseProgram(self.mesh.program)
            matrix = bt.getRotationMatrix('z', self.angle)
            matrix2 = bt.getRotationMatrix('x', self.angle * 2)
            gl.glUniformMatrix4fv(self.model, 1, False, matrix2 @ matrix)
            self.runFunc(self)
            gl.glUseProgram(0)
            self.angle += 0.4
            glfw.swap_buffers(self.window)
            time.sleep(0.017)
        glfw.terminate()

    def runFunc(self):
        pass
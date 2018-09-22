import glfw
import OpenGL.GL as gl
import glEngine.buffers
import sys
from OpenGL.GL import shaders
import trimesh


WIDTH = 800
HEIGHT = 600

vertexShader = """
attribute vec3 position;
attribute vec4 color;
varying vec4 vColor;

void main(void)
{
    vColor = color;
    gl_Position = vec4(position, 1.0);
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
    def __init__(self):
        if not glfw.init():
            sys.exit()

        self.window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

        if not self.window:
            glfw.terminate()
            sys.exit()

        glfw.make_context_current(self.window)

        self.program = shaders.compileProgram(
            shaders.compileShader(vertexShader, gl.GL_VERTEX_SHADER),
            shaders.compileShader(fragmentShader, gl.GL_FRAGMENT_SHADER)
        )

        #self.mesh = trimesh.load('tube.obj')

    def initFunc(self):
        pass

    def run(self):
        self.initFunc(self)
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            self.runFunc(self)
            glfw.swap_buffers(self.window)
        glfw.terminate()

    def runFunc(self):
        pass
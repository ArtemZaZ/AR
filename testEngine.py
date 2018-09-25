import OpenGL.GL as gl
import numpy as np
import trimesh
from glEngine.model import Mesh
from glEngine.base import baseTransformations as bt
from glEngine.variables import Uniform
import sys
import glfw
import time
WIDTH = 800
HEIGHT = 600

vertexShader = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;
attribute vec3 position;

void main(void)
{
    gl_Position = perspective * view * model * vec4(position, 1.0);
}

"""

fragmentShader = """
void main()
{
    gl_FragColor = vec4(0.5, 0.5, 0.5, 1.0);
}
"""

if not glfw.init():
    sys.exit()

window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)

mesh = trimesh.load('models/1002_tray_bottom.STL')

model = Mesh(vertexShader=vertexShader, fragmentShader=fragmentShader, vertices=("position", mesh.vertices),
             faces=mesh.faces)
model.create()

perspectiveU = Uniform("perspective", model.program, gl.GL_FLOAT_MAT4, bt.getPerspectiveMatrix(90, 1000, 1, WIDTH / HEIGHT))
modelU = Uniform("model", model.program, gl.GL_FLOAT_MAT4, np.eye(4))
viewU = Uniform("view", model.program, gl.GL_FLOAT_MAT4, bt.getTranslationMatrix(0, 0, -300))

perspectiveU.create()
modelU.create()
viewU.create()


angle = 0.0
while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glUseProgram(model.program)
    modelU.data = bt.getRotationMatrix('z', angle) @ bt.getRotationMatrix('x', angle * 2)
    modelU.update()
    model.draw(mode=gl.GL_TRIANGLES)
    angle += 0.4
    gl.glUseProgram(0)
    glfw.swap_buffers(window)
    time.sleep(0.017)
glfw.terminate()

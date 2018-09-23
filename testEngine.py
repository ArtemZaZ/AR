import OpenGL.GL as gl
import glEngine.TestClass as Test
import numpy as np
from glEngine.buffers import VertexBuffer, IndexBuffer
from glEngine.arrays import VertexArray
import trimesh
from glEngine.model import Mesh

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
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

mesh = trimesh.load('models/1002_tray_bottom.STL')


def init(self):
    self.mesh = Mesh(vertexShader=vertexShader, fragmentShader=fragmentShader, vertices=mesh.vertices,
                     faces=mesh.faces)
    self.mesh.create()


def run(self):
    self.mesh.draw(mode=gl.GL_TRIANGLES)


test = Test.Test(init, run)

test.initFunc = init
test.runFunc = run

test.run()

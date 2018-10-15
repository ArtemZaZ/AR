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
uniform vec3 lightPos;
uniform vec3 color;
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vLightPos;
varying vec3 vColor;
varying mat4 vModel;
varying mat4 vView;
varying mat4 vPerspective;

void main(void)
{
    vNormal = normal;
    vLightPos = lightPos;
    vColor = color;
    vPosition = position;
    vModel = model;
    vView = view;
    vPerspective = perspective;
    gl_Position = perspective * view * model * vec4(position, 1.0);
}
"""

fragmentShader = """
varying vec3 vNormal;
varying vec3 vPosition;
varying vec3 vLightPos;
varying vec3 vColor;
varying mat4 vModel;
varying mat4 vView;
varying mat4 vPerspective;

void main()
{
    vec3 worldPos = (vModel * vec4(vPosition, 1.0)).xyz;
    vec3 lightColor = vec3(1, 1, 1);
    vec3 worldNormal = normalize(vec3(vModel * vec4(vNormal, 0.0)));
    vec3 lightVector = normalize( vLightPos - worldPos );
    float brightness = dot( worldNormal, lightVector );
    gl_FragColor = vec4(brightness * vColor, 1.0);
}
"""

if not glfw.init():
    sys.exit()

window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)

meshF = trimesh.load('models/tube.obj', 'obj')
mesh = meshF
model = Mesh(vertexShader=vertexShader, fragmentShader=fragmentShader, vertices=("position", mesh.vertices),
             faces=mesh.faces, normal=mesh.vertex_normals)
model.create()

perspectiveU = Uniform("perspective", model.program, gl.GL_FLOAT_MAT4, bt.getPerspectiveMatrix(90, 2000, 1, WIDTH / HEIGHT))
modelU = Uniform("model", model.program, gl.GL_FLOAT_MAT4, np.eye(4))
viewU = Uniform("view", model.program, gl.GL_FLOAT_MAT4, bt.getTranslationMatrix(0, 0, -5))
lightPos = Uniform("lightPos", model.program, gl.GL_FLOAT_VEC3, bt.getDecartVector(0, 0, 20))
color = Uniform("color", model.program, gl.GL_FLOAT_VEC3, bt.getDecartVector(0.0, 0.7, 0.0))
perspectiveU.create()
modelU.create()
viewU.create()
lightPos.create()
color.create()

gl.glEnable(gl.GL_DEPTH_TEST);
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

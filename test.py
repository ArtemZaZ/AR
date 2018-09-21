import glfw
import sys
import OpenGL.GL as gl
import time
import trimesh


if not glfw.init():
    sys.exit()

WIDTH = 800
HEIGHT = 600
window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)


while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    glfw.swap_buffers(window)
    time.sleep(0.017)

glfw.terminate()

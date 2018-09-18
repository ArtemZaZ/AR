import sys
import glfw
import OpenGL.GL as gl
import numpy as np
import ctypes
from OpenGL.GL import shaders
import baseTransformations as bt
import time
import Texture
import View2D
import Sprite
from baseMath import Rectangle
from TextureRegion import TextureRegion
import ViewMaster


if not glfw.init():
    sys.exit()


WIDTH = 800
HEIGHT = 600
window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)


texture = Texture.loadTexture("images/testImage.png")

customSpriteFirst = Sprite.Sprite(Rectangle(0, 0, 0.5, 0.5), TextureRegion(texture, 0.5, 0, 0.5, 0.5))
customSpriteSecond = Sprite.Sprite(Rectangle(0.5, 0.5, 0.5, 0.5), TextureRegion(texture, 0, 0, 1, 0.5))


viewBoxFirst = View2D.View2D(0, 0, WIDTH / 2, HEIGHT)
viewBoxSecond = View2D.View2D(WIDTH / 2, 0, WIDTH / 2, HEIGHT)



def renderFirst(viewBox):
    customSpriteFirst.draw()


def renderSecond(viewBox):
    customSpriteSecond.draw()


viewBoxFirst.render = renderFirst
viewBoxSecond.render = renderSecond
VM = ViewMaster.ViewMaster()
VM.append(viewBoxFirst)
VM.append(viewBoxSecond)

while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    VM.drawAll()
    glfw.swap_buffers(window)
    time.sleep(0.01)

glfw.terminate()
viewBoxFirst.exit()
viewBoxSecond.exit()

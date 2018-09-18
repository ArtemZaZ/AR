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
spriteTexture = Texture.loadTexture("images/testSpriteImage.png")

customSpriteFirst = Sprite.Sprite(Rectangle(-1, 1, 2, 2), TextureRegion(texture, 0, 0, 1, 1))
customSpriteSecond = Sprite.Sprite(Rectangle(0, 0, 0.5, 0.5), TextureRegion(spriteTexture, 0, 0, 1/8, 1/2))


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

i = 0

while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    VM.drawAll()
    customSpriteSecond.rectangle.position = (i, i)
    if int(i*5000) % 10 == 0:
        print(int(i*10))
        customSpriteSecond.textureRegion.x += 1/8
        if customSpriteSecond.textureRegion.x > 1:
            customSpriteSecond.textureRegion.x = 0
    customSpriteSecond.updateAttributes()
    glfw.swap_buffers(window)
    time.sleep(0.017)
    i += 0.0010
    if i > 500:
        viewBoxSecond.hide()
    if i > 1000:
        viewBoxSecond.show()

glfw.terminate()
viewBoxFirst.exit()
viewBoxSecond.exit()

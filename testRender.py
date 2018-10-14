import sys
import glfw
import OpenGL.GL as gl
import time
from user import View2D
from glEngine import sprite, viewMaster, texture
from glEngine.base.baseMath import Rectangle
from glEngine.textureRegion import TextureRegion
from user.battery import Battery

if not glfw.init():
    sys.exit()


WIDTH = 800
HEIGHT = 600
window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)

if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)


tex = texture.loadTexture("images/testImage.png")
spriteTexture = texture.loadTexture("images/testSpriteImage.png")

customSpriteFirst = sprite.Sprite(Rectangle(-1, 1, 2, 2), TextureRegion(tex, 0, 0, 1, 1))
battery = Battery()
customSpriteSecond = sprite.Sprite(Rectangle(0, 0, 0.5, 1), TextureRegion(spriteTexture, 0, 0, 1 / 8, 1 / 2))
customSpriteFirst.create()
battery.create()
customSpriteSecond.create()

viewBoxFirst = View2D.View2D(0, 0, WIDTH, HEIGHT)
viewBoxSecond = View2D.View2D(WIDTH/2, HEIGHT/2, WIDTH/2, HEIGHT/2)
batteryBox = View2D.View2D(WIDTH - 40, HEIGHT - 40, 40, 40)


def renderFirst(viewBox):
    customSpriteFirst.draw()


def renderSecond(viewBox):
    customSpriteSecond.draw()


def renderBattery(viewBox):
    battery.draw()


viewBoxFirst.render = renderFirst
viewBoxSecond.render = renderSecond
batteryBox.render = renderBattery

VM = viewMaster.ViewMaster()
VM.append(viewBoxFirst)
VM.append(viewBoxSecond)
VM.append(batteryBox)

i = 110

while not glfw.window_should_close(window):
    glfw.poll_events()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    VM.drawAll()
    battery.percent = i
    i -= 0.4

    customSpriteSecond.rectangle.position = ((110-i)/110, (110-i)/110 + 0.4)
    if int(i) % 2 == 0:
        customSpriteSecond.textureRegion.x += 1/8
        if customSpriteSecond.textureRegion.x > 1:
            customSpriteSecond.textureRegion.x = 0
        customSpriteSecond.update()

    if i <= 0:
        i = 110
    glfw.swap_buffers(window)
    time.sleep(0.017)

glfw.terminate()
viewBoxFirst.exit()
viewBoxSecond.exit()
batteryBox.exit()

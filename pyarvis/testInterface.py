# -*- coding: utf-8 -*-
import sys

from vispy import gloo, scene, app
from vispy.app import Timer
from vispy.io import read_png
from vispy.scene import SceneCanvas
from vispy.util import load_data_file
from vispy.color import Color
from vispy.visuals import CubeVisual, transforms

from pyarvis import battery
from pyarvis.thermometer import Thermometer


class MySceneCanvas(SceneCanvas):
    def __init__(self, *args, **kwargs):
        self.cube = CubeVisual(size=(0.8, 0.5, 0.5), color='red',
                               edge_color="k")
        self.theta = 0
        self.phi = 0
        self.cube_transform = transforms.MatrixTransform()
        self.cube.transform = self.cube_transform

        self._timer = Timer('auto', connect=self.on_timer, start=True)
        SceneCanvas.__init__(self, *args, **kwargs)

    def on_draw(self, event):
        SceneCanvas.on_draw(self, event)
        # self.cube.draw()

    def on_resize(self, event):
        SceneCanvas.on_resize(self, event)
        vp = (0, 0, self.physical_size[0], self.physical_size[1])
        self.context.set_viewport(*vp)
        self.cube.transforms.configure(canvas=self, viewport=vp)

    def on_timer(self, event):
        self.theta += .5
        self.phi += .5
        self.cube_transform.reset()
        self.cube_transform.rotate(self.theta, (0, 0, 1))
        self.cube_transform.rotate(self.phi, (0, 1, 0))
        self.cube_transform.scale((100, 100, 0.0001))
        self.cube_transform.translate((200, 200))
        self.update()


canvas = MySceneCanvas('Cube', keys='interactive',
                       size=(400, 400))

view = scene.widgets.ViewBox(parent=canvas.scene, name='vb1',
                             margin=2, border_color='red')
view.camera = 'panzoom'
view.camera.flip = (0, 1, 0)
view.size = canvas.size

interpolation = 'nearest'

imageViewBox = scene.ViewBox(parent=view.scene, name="ivb")
imageViewBox.pos = 0, 0
imageViewBox.size = 1, 1
imageViewBox.camera = 'panzoom'
imageViewBox.camera.flip = (0, 1, 0)
imageViewBox.camera.rect = (-1, -1, 2, 2)
imageViewBox.camera.interactive = True

cubeViewBox = scene.ViewBox(parent=view.scene, name='cvb', border_width=2e-3,
                            margin=0.02, border_color='green')
cubeViewBox.interactive = True

#spr = battery.Battery(parent=imageViewBox.scene)
therm = Thermometer(parent=imageViewBox.scene)

cubeViewBox.pos = 0, 0
cubeViewBox.size = 1, 1
cubeViewBox.camera = 'turntable'
cubeViewBox.camera.rect = (-1, -1, 2, 2)
cubeViewBox.camera.interactive = True

color = Color("#3f51b5ff")


# cube = scene.visuals.Cube(size=1, color=color, edge_color="black",
#                          parent=cubeViewBox.scene)
# spr.rect = (0, 0, 0.5, 0.5)
# spr.depth = -1.0


@canvas.events.key_press.connect
def on_key_press(event):
    k = event.text
    if k == '1':
        spr.percent = 100
    if k == '2':
        spr.percent = 75
    if k == '3':
        spr.percent = 50
    if k == '4':
        spr.percent = 25
    if k == '5':
        spr.percent = 15
    if k == '6':
        spr.percent = 5
    if k == '7':
        spr.percent = -1


temp = 0


def on_timer(event):
    global temp
    therm.temperature = temp
    temp += 1


timer = app.Timer(1.0, connect=on_timer, start=True)

canvas.show()
if __name__ == '__main__' and sys.flags.interactive == 0:
    if sys.flags.interactive != 1:
        canvas.app.run()

import sys
from itertools import cycle

import vispy
import cv2
from vispy import io, scene
from vispy.app import Timer
from vispy.color import BaseColormap, get_colormaps
from vispy.scene import SceneCanvas, ViewBox, STTransform, Console
import numpy as np

from pyarvis.sprite import Sprite


class TransFire(BaseColormap):
    glsl_map = """
    vec4 translucent_fire(float t) {
        return vec4(pow(t, 0.5), t, t*t, max(0, t*1.05 - 0.05));
    }
    """


class TransGrays(BaseColormap):
    glsl_map = """
    vec4 translucent_grays(float t) {
        return vec4(t, t, t, t*0.05);
    }
    """


cap = cv2.VideoCapture(0)
_, frame = cap.read()

vol1 = np.load(io.load_data_file('volume/stent.npz'))['arr_0']
vol2 = np.load(io.load_data_file('brain/mri.npz'))['data']
vol2 = np.flipud(np.rollaxis(vol2, 1))

canvas = SceneCanvas("nirterface", keys='interactive', size=(800, 600), show=True)
canvas.measure_fps()

view = canvas.central_widget.add_view()
# view = canvas.central_widget.add_view()
#view = ViewBox(parent=canvas.scene, name='vb1',
#               margin=2, border_color='red')
#view.size = canvas.size

backgroundView = ViewBox(parent=view.scene, name="vb2",
                         margin=2, border_color='green')
backgroundView.size = view.size
backgroundView.camera = 'panzoom'
backgroundView.camera.flip = (0, 1, 0)
backgroundView.camera.rect = (-1, -1, 2, 2)
backgroundView.interactive = True

background = Sprite(frame, parent=backgroundView.scene)

volumeView = ViewBox(parent=view.scene, name="vb3",
                     margin=2, border_color='blue')
volumeView.size = canvas.size
volumeView.interactive = True

emulate_texture = False
volume1 = scene.visuals.Volume(vol1, parent=volumeView.scene, threshold=0.225,
                               emulate_texture=emulate_texture)
volume1.transform = scene.STTransform(translate=(64, 64, 0))
volume2 = scene.visuals.Volume(vol2, parent=volumeView.scene, threshold=0.2,
                               emulate_texture=emulate_texture)
volume2.visible = False
fov = 45.

cam2 = scene.cameras.TurntableCamera(parent=volumeView.scene, fov=fov,
                                     name='Turntable')
volumeView.camera = cam2
axis = scene.visuals.XYZAxis(parent=volumeView)
s = STTransform(translate=(50, 50), scale=(50, 50, 50, 1))
affine = s.as_matrix()
axis.transform = affine

opaque_cmaps = cycle(get_colormaps())
translucent_cmaps = cycle([TransFire(), TransGrays()])
opaque_cmap = next(opaque_cmaps)
translucent_cmap = next(translucent_cmaps)

console = Console(text_color='black', font_size=12., parent=canvas.scene)
console.pos = 600, 0
console.size = 400, 400
console.write("ILIJA PIDOR")


def on_timer(event):
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    background.data = frame
    cam2.azimuth += 1
    #axis.transform.reset()
    #axis.transform.rotate(cam2.roll, (0, 0, 1))
    #axis.transform.rotate(cam2.elevation, (1, 0, 0))
    #axis.transform.rotate(cam2.azimuth, (0, 1, 0))
    canvas.update()


# Implement key presses
@canvas.events.key_press.connect
def on_key_press(event):
    global opaque_cmap, translucent_cmap
    if event.text == '2':
        methods = ['mip', 'translucent', 'iso', 'additive']
        method = methods[(methods.index(volume1.method) + 1) % 4]
        print("Volume render method: %s" % method)
        cmap = opaque_cmap if method in ['mip', 'iso'] else translucent_cmap
        volume1.method = method
        volume1.cmap = cmap
        volume2.method = method
        volume2.cmap = cmap
    elif event.text == '3':
        volume1.visible = not volume1.visible
        volume2.visible = not volume1.visible
    elif event.text == '4':
        if volume1.method in ['mip', 'iso']:
            cmap = opaque_cmap = next(opaque_cmaps)
        else:
            cmap = translucent_cmap = next(translucent_cmaps)
        volume1.cmap = cmap
        volume2.cmap = cmap
    elif event.text != '' and event.text in '[]':
        s = -0.025 if event.text == '[' else 0.025
        volume1.threshold += s
        volume2.threshold += s
        th = volume1.threshold if volume1.visible else volume2.threshold
        print("Isosurface threshold: %0.3f" % th)


timer = Timer('auto', connect=on_timer, start=True)

canvas.show()
if __name__ == '__main__' and sys.flags.interactive == 0:
    if sys.flags.interactive != 1:
        canvas.app.run()

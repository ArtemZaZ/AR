import OpenGL.GL as gl
import ViewBox as vb
import baseTransformations as bt


class View2D(vb.ViewBox):
    def __init__(self, x=0, y=0, width=100, height=100, z=0):
        vb.ViewBox.__init__(self, x, y, width, height, z)



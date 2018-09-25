import OpenGL.GL as gl
import numpy as np
from glEngine.model import Mesh
from glEngine.base.baseShaders import *


class Sprite:
    def __init__(self, rectangle=None, textureRegion=None):
        self._rectangle = rectangle
        self._textureRegion = textureRegion
        self.__data = np.zeros(4, [("vertex", np.float32, 2),
                                   ("textureCoordinates", np.float32, 2)])
        self._spriteMesh = Mesh(baseSpriteVertexShader, baseSpriteFragmentShader, ("vertex", self.__data["vertex"]),
                                np.array([0, 1, 2, 2, 1, 3], dtype=np.uint32), textureCoordinates=self.__data["textureCoordinates"])
        self.__updateAttributes()

    def __updateAttributes(self):
        r = self._rectangle
        tr = self._textureRegion
        self.__data["vertex"][...] = (r.x, r.y), (r.x + r.width, r.y), \
                                     (r.x, r.y - r.height), (r.x + r.width, r.y - r.height)

        self.__data["textureCoordinates"][...] = (tr.x, tr.y), (tr.x + tr.width, tr.y), \
                                                 (tr.x, tr.y - tr.height), (tr.x + tr.width, tr.y - tr.height)

    def create(self):
        self._spriteMesh.create()

    def update(self):
        self.__updateAttributes()
        self._spriteMesh.update()

    @property
    def rectangle(self):
        """
        Через свойство можно изменить параметры объекта, т.к. возвращается ссылка на него
        :return:
        """
        return self._rectangle

    @rectangle.setter
    def rectangle(self, rectangle):
        self._rectangle = rectangle

    @property
    def textureRegion(self):
        return self._textureRegion

    @textureRegion.setter
    def textureRegion(self, textureRegion):
        self._textureRegion = textureRegion

    def draw(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._textureRegion.texture)
        self._spriteMesh.draw(mode=gl.GL_TRIANGLES)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

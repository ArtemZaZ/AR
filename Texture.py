import OpenGL.GL as gl
from PIL import Image
import numpy as np

"""
class Texture(int):
    def __init__(self, path):
        int.__init__(self, gl.glGenTextures(1))
        image = Image.open(path)
        imageData = np.array(list(image.getdata()), np.uint8)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 4)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BASE_LEVEL, 0)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_LEVEL, 0)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, image.size[0], image.size[1],
         0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, imageData)
"""


def loadTexture(path):
    image = Image.open(path)
    imageData = np.array(list(image.getdata()), np.uint8)
    texture = gl.glGenTextures(1)
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 4)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BASE_LEVEL, 0)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_LEVEL, 0)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.size[0], image.size[1],
                    0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imageData)
    return texture
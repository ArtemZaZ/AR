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
    image = Image.open(path).convert("RGBA")
    imageData = image.tobytes("raw", "RGBA", 0, -1)
    texture = gl.glGenTextures(1)
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 4)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glEnable(gl.GL_BLEND)  # включить смешивание
    gl.glEnable(gl.GL_ALPHA_TEST)  # разрешить прозрачность
    gl.glAlphaFunc(gl.GL_GEQUAL, 0.4)  # не пропускать прозрачность ниже 0.4
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)  # один из видов смешивания, подробнее читать в интернете
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_BASE_LEVEL, 0)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAX_LEVEL, 0)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.size[0], image.size[1],
                    0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imageData)
    return texture
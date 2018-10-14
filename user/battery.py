import glEngine.sprite as sprite
import glEngine.texture as texture
from glEngine.textureRegion import TextureRegion
from glEngine.base.baseMath import Rectangle


class Battery:
    def __init__(self):
        """ Вообще ее нужно в атлас текстур запихать """
        self._texture = texture.loadTexture("images/battery_set_3.png")
        self._percent = 100
        self.__state = "100%"
        self._textureRegionDict = {
            "100%": TextureRegion(self._texture, 0, 0, 1/3, 1/3),
            "75%": TextureRegion(self._texture, 1/3, 0, 1/3, 1/3),
            "50%": TextureRegion(self._texture, 2/3, 0, 1/3, 1/3),
            "25%": TextureRegion(self._texture, 0, 1/3, 1/3, 1/3),
            "15%": TextureRegion(self._texture, 1/3, 1/3, 1/3, 1/3),
            "5%": TextureRegion(self._texture, 2/3, 1/3, 1/3, 1/3),
            "charging": TextureRegion(self._texture, 0, 2/3, 1/3, 1/3)
        }
        self._sprite = sprite.Sprite(Rectangle(-1, 1, 2, 2), self._textureRegionDict.get(self.__state))

    def create(self):
        self._sprite.create()

    @property
    def percent(self):
        return self._percent

    def __setState(self, state):
        if state != self.__state:
            self.__state = state
            self._sprite.textureRegion = self._textureRegionDict.get(self.__state)
            self._sprite.update()

    @percent.setter
    def percent(self, value):
        print(self.__state)
        self._percent = value
        if value > 75:
            self.__setState("100%")
        elif value > 50:
            self.__setState("75%")
        elif value > 25:
            self.__setState("50%")
        elif value > 15:
            self.__setState("25%")
        elif value > 5:
            self.__setState("15%")
        elif value > 0:
            self.__setState("5%")
        else:
            self.__setState("charging")

    def draw(self):
        self._sprite.draw()

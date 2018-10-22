from vispy.io import read_png

from pyarvis.sprite import Sprite


class Battery(Sprite):
    def __init__(self, **kwargs):
        self._textureRegionDict = {
            "100%": (0, 0, 1/3, 1/3),
            "75%": (1/3, 0, 1/3, 1/3),
            "50%": (2/3, 0, 1/3, 1/3),
            "25%": (0, 1/3, 1/3, 1/3),
            "15%": (1/3, 1/3, 1/3, 1/3),
            "5%": (2/3, 1/3, 1/3, 1/3),
            "charging": (0, 2/3, 1/3, 1/3)
        }
        self._percent = 100
        Sprite.__init__(self, read_png("images/battery.png"), **kwargs)
        self.rect = self._textureRegionDict['100%']

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        self._percent = value
        if value > 75:
            self.rect = self._textureRegionDict['100%']
        elif value > 50:
            self.rect = self._textureRegionDict['75%']
        elif value > 25:
            self.rect = self._textureRegionDict['50%']
        elif value > 15:
            self.rect = self._textureRegionDict['25%']
        elif value > 5:
            self.rect = self._textureRegionDict['15%']
        elif value > 0:
            self.rect = self._textureRegionDict['5%']
        else:
            self.rect = self._textureRegionDict['charging']

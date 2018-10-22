from vispy.io import read_png

from sprite import Sprite


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
        Sprite.__init__(self, read_png("battery.png"), **kwargs)
        self.rect = self._textureRegionDict['100%']

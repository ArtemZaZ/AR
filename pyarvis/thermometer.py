from vispy.io import read_png
from vispy.scene import Text

from pyarvis.sprite import Sprite


class Thermometer(Sprite):
    def __init__(self, **kwargs):
        self.text = Text("0ºC", font_size=7, bold=True, color='w')
        self._temperature = 0
        Sprite.__init__(self, read_png("images/therm.png"), **kwargs)
        self.text.parent = self.parent
        self.text.pos = (0.2, 0)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        self.text.text = str(value) + "ºC"

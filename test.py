import glass

"""
print(glass.State.Stopped)
glass.State.__stopped = 1
print(glass.State.__stopped)
print(glass.State.Stopped)
"""

import ViewBox

vb = ViewBox.ViewBox()


class Window(ViewBox.ViewBox):
    def __init__(self):
        ViewBox.ViewBox.__init__(self, 0, 0, 0, 0)

    def draw(self):
        print(1)

Window().draw()
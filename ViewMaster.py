import ViewBox as vb


class ViewMaster(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.__sort()   # сортируем окна по глубине

    def drawAll(self):
        for viewBox in self:
            viewBox.swap()

    def __sort(self):
        self.sort(key=lambda viewb: viewb.z)




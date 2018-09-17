import ViewBox as vb


class ViewMaster(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.sort()   # сортируем окна по глубине

    def drawAll(self):
        for viewBox in self:
            viewBox.swap()

    def sort(self, *kwargs):
        list.sort(self, key=lambda viewb: viewb.z)

    def append(self, viewb: vb.ViewBox):
        list.append(self, viewb)
        self.sort()




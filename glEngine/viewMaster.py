from glEngine import viewBox as vb


class ViewMaster(list):
    def __init__(self):
        list.__init__(self)
        self.sort()   # сортируем окна по глубине

    def drawAll(self):
        for viewBox in self:
            viewBox.swap()

    def sort(self, *kwargs):
        list.sort(self, key=lambda viewb: viewb.z)

    def append(self, viewb: vb.ViewBox):
        list.append(self, viewb)
        self.sort()




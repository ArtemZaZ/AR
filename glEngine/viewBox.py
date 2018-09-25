import OpenGL.GL as gl
from glEngine import RTCEventMaster as em, exceptions


class ViewBox:
    def __init__(self, x=0, y=0, width=100, height=100, z=0):
        self._x = int(x)  # координаты viewport
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._z = z  # z - координата окна
        self._visible = True     # отображается ли окно
        self._eventDict = {
            "SHOW": em.EventBlock("SHOW"),  # событие, вызывающееся при вызове show
            "HIDE": em.EventBlock("HIDE"),  # вызове hide
            "CHANGE_Z": em.EventBlock("CHANGE_Z"),   # при изменении Z
            "RESIZE": em.EventBlock("RESIZE"),   # при масштабировании окна
            "CHANGE_POSITION": em.EventBlock("CHANGE_POSITION")     # при изменении позиции окна
        }
        self._eventMaster = em.EventMaster()
        self._eventMaster.appendAll(self._eventDict.values())
        self._eventMaster.start()

    def __del__(self):
        self.exit()

    def show(self):     # показать окно
        self._visible = True
        self._eventDict.get("SHOW").push(self)

    def hide(self):     # скрыть окно
        self._visible = False
        self._eventDict.get("HIDE").push(self)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z
        self._eventDict.get("CHANGE_Z").push(self, self._z)

    def resize(self, width, height):
        self._width = width
        self._height = height
        self._eventDict.get("RESIZE").push(self, self._width, self._height)

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, pos):
        self._x = pos[0]
        self._y = pos[1]
        self._eventDict.get("CHANGE_POSITION").push(self, self._x, self._y)

    def connect(self, toEvent, foo):  # ф-ия подключения обработчика события по имени события
        event = self._eventDict.get(toEvent)
        if not event:  # если в словаре событий нет такого события - ошибка
            raise exceptions.EventError(toEvent + ": There is no such event")
        event.setfun(foo)

    def render(self):     # ф-ия для перегрузки
        pass

    def swap(self):     # рисуем содержимое
        if self._visible:
            gl.glViewport(self._x, self._y, self._width, self._height)
            self.render(self)

    def exit(self):
        self._eventMaster.exit()

import OpenGL.GL as gl
import RTCEventMaster as em
import Exceptions


class ViewBox:
    def __init__(self, x=0, y=0, width=100, height=100, z=0):
        self.x = int(x)  # координаты viewport
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.z = z  # z - координата окна
        self.__visible = True     # отображается ли окно
        self.eventDict = {
            "SHOW": em.EventBlock("SHOW"),  # событие, вызывающееся при вызове show
            "HIDE": em.EventBlock("HIDE"),  # вызове hide
            "CHANGE_Z": em.EventBlock("CHANGE_Z"),   # при изменении Z
            "RESIZE": em.EventBlock("RESIZE"),   # при масштабировании окна
            "CHANGE_POSITION": em.EventBlock("CHANGE_POSITION")     # при изменении позиции окна
        }
        self.eventMaster = em.EventMaster()
        self.eventMaster.appendAll(self.eventDict.values())
        self.eventMaster.start()

    def __del__(self):
        self.exit()

    def show(self):     # показать окно
        self.__visible = True
        self.eventDict.get("SHOW").push(self)

    def hide(self):     # скрыть окно
        self.__visible = False
        self.eventDict.get("HIDE").push(self)

    def setZ(self, z):
        self.z = z
        self.eventDict.get("CHANGE_Z").push(self, z)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.eventDict.get("RESIZE").push(self, width, height)

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.eventDict.get("CHANGE_POSITION").push(self, x, y)

    def connect(self, toEvent, foo):  # ф-ия подключения обработчика события по имени события
        event = self.eventDict.get(toEvent)
        if not event:  # если в словаре событий нет такого события - ошибка
            raise Exceptions.EventError(toEvent + ": There is no such event")
        event.setfun(foo)

    def render(self):     # ф-ия для перегрузки
        pass

    def swap(self):     # рисуем содержимое
        if self.__visible:
            gl.glViewport(self.x, self.y, self.width, self.height)
            self.render(self)

    def exit(self):
        self.eventMaster.exit()

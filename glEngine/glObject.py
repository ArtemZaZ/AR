
class GLObject(object):
    """
    Базовый класс для gl объектов
    """
    def __init__(self):
        self._descriptor = None   # дескриптор объекта
        self._isCreated = False     # создан ли объект
        self._type = None   # тип объекта (текстура, буффер и т.п.)

    def create(self):
        """ Creation GL Object"""
        if not self._isCreated:
            self._create()
            self._isCreated = True

    def _create(self):
        """ function to override """
        pass

    def update(self):
        """ update GL Object """
        if self._isCreated:
            self._update()

    def _update(self):
        """ function to override """
        pass

    @property
    def type(self):
        return self._type

    @property
    def descriptor(self):
        return self._descriptor

    def _bind(self):
        """ function to override """
        pass

    def bind(self):
        """ активация данного объекта """
        self._bind()

    def unbind(self):
        """ дезактивация данного объекта """
        self._unbind()

    def _unbind(self):
        """ function to override """
        pass


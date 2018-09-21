

class GLObject(object):
    def __init__(self):
        self._descriptor = None   # дескриптор объекта
        self._isCreated = False
        self._type = None   # тип объекта

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


import serial
import threading
import RTCEventMaster


class EventError(Exception):  # Ошибка события
    pass


class __GlassState:   # структура состояние очков
    # псевдо-приватные переменные
    __stopped = 0   # очки остановлены
    __reading = 1   # производится чтение углов
    __exit = 2      # был выход из программы
    __error = 3     # произошла ошибка

    # их геттеры
    @property
    def Stopped(self):
        return self.__stopped

    @property
    def Reading(self):
        return self.__reading

    @property
    def Exit(self):
        return self.__exit

    @property
    def Error(self):
        return self.__error


State = __GlassState()  # глобальная переменная состояния, переменные можно только читать


class Glass(threading.Thread):
    def __init__(self, portName):
        threading.Thread.__init__(self)
        self.port = serial.Serial(portName, baudrate=115200)
        # TODO: убрать привязку к data
        self.data = [0, 0, 0]   # данные
        self.primatyData = [0, 0, 0]    # начальные углы
        self.state = State.Stopped    # ставвим начальное положение - остановлен
        self.startFlag = False  # метка нажатия кнопки старт
        self.eventDict = {  # Словарь событий
            "START": RTCEventMaster.EventBlock("START"),  # событие начала работы
            "STOP": RTCEventMaster.EventBlock("STOP"),  # событие окончания работы
            "EXIT": RTCEventMaster.EventBlock("EXIT"),  # событие выхода из потока
            "READ": RTCEventMaster.EventBlock("READ"),  # события чтения углов
            "ERROR": RTCEventMaster.EventBlock("ERROR")  # событие ошибки чтения углов
        }
        self.eventMaster = RTCEventMaster.EventMaster()     # создаем мастера событий
        self.eventMaster.append(self.eventDict.get("START"))    # привязываем обработчики
        self.eventMaster.append(self.eventDict.get("STOP"))
        self.eventMaster.append(self.eventDict.get("EXIT"))
        self.eventMaster.append(self.eventDict.get("READ"))
        self.eventMaster.append(self.eventDict.get("ERROR"))
        self.eventMaster.start()

    def connectFunction(self, toEvent, foo):     # ф-ия подключения обработчика события по имени события
        event = self.eventDict.get(toEvent)
        if not event:
            raise EventError(toEvent + ": There is no such event")

        def voidFoo():  # Все обработчики событий имеют в качестве параметра 1 аргумент
            foo(self.data)

        event.setfun(voidFoo)

    def exit(self):
        self.state = State.Exit
        self.eventDict.get("EXIT").push()
        self.eventMaster.exit()
        self.port.close()

    def _readMessage(self):
        buf = ''    # временный буффер
        temp = self.port.read()     # читаем побайтово
        while temp != b'<':     # читаем пока не найдем вхождение
            temp = self.port.read()
        temp = self.port.read()
        while temp != b'>':
            if temp == b'<':
                return None
            buf += temp
            temp = self.port.read()
        return buf

    def _parseMessage(self, message):
        try:
            listbuf = list(map(bytes, message.split()))     # разделение сообщения на токены и запись их в список
            if listbuf[0] == b'ypr':
                newData = [float(i) for i in listbuf[1:]]
                if self.startFlag:  # если была нажата кнопка старт
                    self.primatyData = self.newData[:]     # устанавливаем начальные данные
                    self.startFlag = False

                if self.state is State.Reading:     # если уже производится чтение углов
                    # TODO: убрать хрень с привязкой к data
                    self.data = [newData[0] - self.primatyData[0], newData[1] - self.primatyData[1],
                                 newData[2] - self.primatyData[2]]
                    self.eventDict.get("READ").push()

            elif listbuf[0] == b'*':  # если сообщение начинается с *
                print("COMMENT: " + str(message))  # вывод комментария

            elif listbuf[0] == b'start':
                self.eventDict.get("START").push()
                self.startFlag = True
                self.state = State.Reading

            elif listbuf[0] == b'stop':   # если пришло сообщение stop(была нажата кнопка stop)
                self.primatyData = [0, 0, 0]    # сбросить текущие углы
                self.eventDict.get("STOP").push()   # вызвать событие нажатия кнопки стоп
                self.state = State.Stopped
        except:
            # TODO: Переделать EventMaster с вызовом аргументов через push(*args)
            self.eventDict.get("ERROR").push()

    def run(self):
        self.port.write(b'g')   # отправляем любой символ - готовы читать
        while self.state is not State.Exit:
            message = self._readMessage()
            if message is not None:
                self._parseMessage(message)


if __name__ == "__main__":
    def startHandler(data):
        print("I started!")

    def stopHandler(data):
        print("I stopped!")

    def readHandler(data):
        print(data)

    glass = Glass("/dev/ttyUSB0")
    glass.connectFunction("START", startHandler)
    glass.connectFunction("STOP", stopHandler)
    glass.connectFunction("READ", readHandler)
    glass.start()

import enum

class AudioEnum(enum.Enum):
    background = 0
    run = 1
    jump = 2
    beat = 3
    damage = 4
    
class Observer:
    def onNotify(self):
        pass

class Audio(Observer):
    def onNotify(self, sound):
        if(sound == AudioEnum.run.name):
            print("play 'run'")
        if(sound == AudioEnum.jump.name):
            print("play 'jump'")
        if(sound == AudioEnum.beat.name):
            print("play 'beat'")

class Subject:
    def __init__(self):
        self.__observers = []
        self.__observersCounter = 0

    def notify(self, event):
        for observer in self.__observers:
            observer.onNotify(event)

    def addObserver(self, newObserver):
        if newObserver not in self.__observers:
            self.__observers.append(newObserver)
            self.__observersCounter += 1

    def removeObserver(self, newObserver):
        try:
            self.__observers.remove(newObserver)
            self.__observersCounter -= 1
        except ValueError:
            pass

    @property
    def getObserversCounter(self):
        return self.__observersCounter

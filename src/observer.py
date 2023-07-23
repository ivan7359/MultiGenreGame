from config import *

class Observer:
    def onNotify(self):
        pass

class Audio(Observer):
    def __init__(self, assetManager):
        self.__assetManager = assetManager

    def onNotify(self, event):
        if (event == EventsEnum.movement.value):
            self.__assetManager.getSound('Running').play()

        if (event == EventsEnum.jump.value):
            self.__assetManager.getSound('Jump').play()

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


#AMMM PROJECT
#Representation of a driver
#Copyright 2018 Elena Molina & Miguel Álvarez
#Based on: AMMM Lab Heuristics v1.2 Copyright 2018 Luis Velasco.


class Driver(object):
    def __init__(self, driverId):
        self._driverId = driverId
        self._maxMin = 0  # maxMin of that driver


    def getId(self):
        return(self._driverId)

    def getMaxMin(self):
        return(self._maxMin)

    def addMaxMin(self, maxMin):
        self._maxMin = maxMin

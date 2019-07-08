
#AMMM PROJECT
#Representation of a service
#Copyright 2018 Elena Molina & Miguel Álvarez
#Based on: AMMM Lab Heuristics v1.2 Copyright 2018 Luis Velasco.


class Service(object):
    def __init__(self, serviceId):
        self._serviceId = serviceId
        self._startTime = 0  # startTime of that service
        self._min = 0  # min of that service
        self._km = 0  # km of that service
        self._load = 0  # load per km of that service

    def getId(self):
        return(self._serviceId)

    def getStartTime(self):
        return(self._startTime)

    def getMin(self):
        return(self._min)

    def getKm(self):
        return(self._km)

    def getLoad(self):
        return(self._load)

    def addStartTimeandMinandKmandLoad(self, startTime, min, km, load):
        self._startTime = startTime
        self._min = min
        self._km = km
        self._load = load

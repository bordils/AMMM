
#AMMM PROJECT
#Representation of a bus
#Copyright 2018 Elena Molina & Miguel Álvarez
#Based on: AMMM Lab Heuristics v1.2 Copyright 2018 Luis Velasco.


class Bus(object):
    def __init__(self, busId):
        self._busId = busId
        self._capacity = 0 # capacity of that bus
        self._CPM = 0 # cost per min of that bus
        self._CPKm = 0  # cost per km of that bus

    def getId(self):
        return(self._busId)

    def getBusCapacity(self):
        return(self._capacity)

    def getBusCPM(self):
        return(self._CPM)

    def getBusCPKm(self):
        return(self._CPKm)

    def addCapacityandCPMandCPKm(self, capacity, CPM, CPKm):
        self._capacity = capacity
        self._CPM = CPM
        self._CPKm = CPKm
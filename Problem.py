'''
AMMM PROJECT
Representation of a problem instance.
Copyright 2018 Elena Molina & Miguel Álvarez
Based on: AMMM Lab Heuristics v1.2 Copyright 2018 Luis Velasco.
'''

from Service import Service
from Bus import Bus
from Driver import Driver

class Problem(object):
    def __init__(self, inputData):
        self.inputData = inputData

        nServices=self.inputData.nServices
        sStartTime=self.inputData.sStartTime
        sMin=self.inputData.sMin
        sKM=self.inputData.sKM
        sLoad=self.inputData.sLoad

        nBuses=self.inputData.nBuses
        bCap=self.inputData.bCap
        bCPM=self.inputData.bCPM
        bCPKm=self.inputData.bCPKm
        maxBuses=self.inputData.maxBuses

        nDrivers=self.inputData.nDrivers
        dMaxMin=self.inputData.dMaxMin

        BM=self.inputData.BM
        CBM=self.inputData.CBM
        CEM=self.inputData.CEM

        self.services = []                             # vector with services
        for sId in range(0, nServices):               # sId = 0..(nServices-1)
            service = Service(sId)
            service.addStartTimeandMinandKmandLoad(sStartTime[sId], sMin[sId], sKM[sId], sLoad[sId])
            self.services.append(service)

        self.minPerBusId = [0] * nBuses      # vector with min for each Bus. initialized to nBuses zeros [ 0 ... 0 ]
        self.minPerDriverId = [0] * nDrivers      # vector with min for each Driver. initialized to nDrivers zeros [ 0 ... 0 ]
        self.buses = []                              # vector with buses
        for bId in range(0, nBuses):                # bId = 0..(nBuses-1)
            bus = Bus(bId)
            bus.addCapacityandCPMandCPKm(bCap[bId], bCPM[bId], bCPKm[bId])
            self.buses.append(bus)

        self.drivers = []                              # vector with drivers
        for dId in range(0, nDrivers):                # bId = 0..(nDrivers-1)
            driver = Driver(dId)
            driver.addMaxMin(dMaxMin[dId])
            self.drivers.append(driver)

        self.maxBuses=maxBuses
        self.BM=BM
        self.CBM=CBM
        self.CEM=CEM

    def getServices(self):
        return(self.services)

    def getBuses(self):
        return(self.buses)

    def getDrivers(self):
        return(self.drivers)

    def checkInstance(self):
        totalServicesLoad = 0
        for service in self.services:
            totalServicesLoad+=service.getLoad()
        totalBusesCapacity = 0
        for bus in self.buses:
            totalBusesCapacity+=bus.getBusCapacity()
        if(totalBusesCapacity < totalServicesLoad): return(False)

        totalServicesMin = 0
        for service in self.services:
            totalServicesMin+=service.getMin()
        totalDriversMin = 0
        for driver in self.drivers:
            totalDriversMin+=driver.getMaxMin()
        if(totalDriversMin < totalServicesMin): return(False)
        
        return(True)

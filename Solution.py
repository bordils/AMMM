'''
AMMM PROJECT
Representation of a solution instance.
Copyright 2018 Elena Molina & Miguel Álvarez
Based on: AMMM Lab Heuristics v1.2 Copyright 2018 Luis Velasco.
'''

import copy, time
from Problem import Problem

# Assignment class stores the cost 
# when a bus and driver are assigned to a service.  
class Assignment(object):
    def __init__(self, sId, bId, dId, cost):
        self.serviceId = sId
        self.busId = bId
        self.driverId = dId
        self.cost = cost

# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(Problem):
    @staticmethod
    def createEmptySolution(config, problem):
        solution = Solution(problem.inputData)
        solution.setVerbose(config.verbose)
        return(solution)

    def __init__(self, inputData):
        super(Solution, self).__init__(inputData)
        
        self.busIdtoServiceID = {}             # hash table: bus Id => service Id (may be an array)
        self.driverIdtoServiceID = {}         # hash table: driver Id => service Id (may be an array)
        self.serviceIdtoBusIDDriverId = {}  #  hash table: service Id => array [bus Id, driver ID]

        # vector with min for each Bus. initialized to nBuses zeros [ 0 ... 0 ]
        self.minPerBusId = copy.deepcopy(self.minPerBusId)
        
        # vector with min for each Driver. initialized to nDrivers zeros [ 0 ... 0 ]
        self.minPerDriverId = copy.deepcopy(self.minPerDriverId)

        self.cost = 0.0
        
        self.feasible = True
        self.verbose = False
    
        self.numUsedBuses = 0
        self.availableNumBuses=0

    def setVerbose(self, verbose):
        if(not isinstance(verbose, (bool)) or (verbose not in [True, False])):
            raise Exception('verbose(%s) has to be a boolean value.' % str(verbose))
        self.verbose = verbose
    
    def makeInfeasible(self):
        self.feasible = False
        self.cost = float('infinity')
    
    def isFeasible(self):
        return(self.feasible)
    
    def updateCost(self):
        self.cost = 0.0
        
        for driver in self.drivers:
            driverWorkedTime = 0.0
            dId = driver.getId()
            if (dId in self.driverIdtoServiceID):
                for serv in self.driverIdtoServiceID[dId]:
                    driverWorkedTime+=self.services[serv].getMin()

                if (driverWorkedTime > self.BM): # worked extra min
                    self.cost+=self.BM*self.CBM+(driverWorkedTime-self.BM)*self.CEM
                else:
                    self.cost+=driverWorkedTime*self.CBM

        for bus in self.buses:
            bId = bus.getId()
            if (bId in self.busIdtoServiceID):
                for serv in self.busIdtoServiceID[bId]:
                    self.cost+=self.services[serv].getMin()*bus.getBusCPM()+self.services[serv].getKm()*bus.getBusCPKm()
    
    def isFeasibleToAssignServicetoBus(self, sId, bId):
        if(sId in self.serviceIdtoBusIDDriverId):
            if(self.verbose): print('Service(%s) already has a bus and driver assigned.' % str(sId))
            return(False)

        service = self.services[sId]
        load = service.getLoad()
        bus = self.buses[bId]
        capacity = bus.getBusCapacity()

        if(capacity < load):
            if(self.verbose): print('Bus(%s) does not has enough available capacity for Service(%s)' % (str(bId), str(sId)))
            return(False)

        startTime= service.getStartTime()
        if (bId in self.busIdtoServiceID):

            for servId in self.busIdtoServiceID[bId]:
                serv=self.services[servId]
                prevStartTime=serv.getStartTime()
                prevDuration=serv.getMin()
                prevFinish=prevStartTime+prevDuration
                if (startTime<prevFinish):
                    return(False)

        return(True)
    def isFeasibleToAssignServicetoDriver(self, sId, dId):
        if(sId in self.serviceIdtoBusIDDriverId):
            if(self.verbose): print('Service(%s) already has a bus and driver assigned.' % str(sId))
            return(False)
        
        service = self.services[sId]
        duration = service.getMin()
        driver = self.drivers[dId]
        availableTime = driver.getMaxMin()
        if (dId in self.driverIdtoServiceID):
            for serv in self.driverIdtoServiceID[dId]:
                availableTime-=self.services[serv].getMin()
        if(availableTime < duration):
            if(self.verbose): print('Driver(%s) does not has enough available time for Service(%s)' % (str(dId), str(sId)))
            return(False)        
        startTime= service.getStartTime()
        if (dId in self.driverIdtoServiceID):
            for servId in self.driverIdtoServiceID[dId]:
                serv=self.services[servId]
                prevStartTime=serv.getStartTime()
                prevDuration=serv.getMin()
                prevFinish=prevStartTime+prevDuration
                if (startTime<prevFinish):
                    return(False)
        return(True)

    def getBusAssignedToService(self, sId):
        if(sId not in self.serviceIdtoBusIDDriverId): return(None)
        return(self.serviceIdtoBusIDDriverId[sId][0])

    def getDriverAssignedToService(self, sId):
        if(sId not in self.serviceIdtoBusIDDriverId): return(None)
        return(self.serviceIdtoBusIDDriverId[sId][1])

    def assign(self, sId, bId, dId):
        if(not self.isFeasibleToAssignServicetoBus(sId, bId)):
            if(self.verbose): print('Unable to assign Servive(%s) to Bus(%s)' % (str(sId), str(bId)))
            return(False)

        if(not self.isFeasibleToAssignServicetoDriver(sId, dId)):
            if(self.verbose): print('Unable to assign Servive(%s) to Driver(%s)' % (str(sId), str(dId)))
            return(False)

        if (bId not in self.busIdtoServiceID):
            if (self.numUsedBuses+1<=self.maxBuses):
                self.busIdtoServiceID[bId]=[] 
                self.numUsedBuses += 1
            else:
                if(self.verbose): print('Unable to assign Servive(%s) to Bus(%s)' % (str(sId), str(bId)))
                return(False)

        self.busIdtoServiceID[bId].append(sId)
        if (dId not in self.driverIdtoServiceID): self.driverIdtoServiceID[dId]=[]
        self.driverIdtoServiceID[dId].append(sId)  
        self.serviceIdtoBusIDDriverId[sId] =[bId,  dId]  

        self.updateCost()
        return(True)

    def isFeasibleToUnassignBusFromService(self, bId, sId):

        if(sId not in self.serviceIdtoBusIDDriverId):
            if(self.verbose): print('Service(%s) is not assigned to any bus.' % str(sId))
            return(False)
        
        if(bId not in self.busIdtoServiceID):
            if(self.verbose): print('Bus(%s) is not used by any service.' % str(bId))
            return(False)

        if(sId not in self.busIdtoServiceID[bId]):
            if(self.verbose): print('Bus(%s) is not used by Service(%s).' % (str(bId), str(sId)))
            return(False)

        return(True)

    def isFeasibleToUnassignDriverFromService(self, dId, sId):
        if(sId not in self.serviceIdtoBusIDDriverId):
            if(self.verbose): print('Service(%s) is not assigned to any driver.' % str(sId))
            return(False)
        
        if(dId not in self.driverIdtoServiceID):
            if(self.verbose): print('Driver(%s) is not used by any service.' % str(bId))
            return(False)

        if(sId not in self.driverIdtoServiceID[dId]):
            if(self.verbose): print('Driver(%s) is not used by Service(%s).' % (str(bId), str(sId)))
            return(False)

        return(True)

    def unassign(self, sId, bId, dId):
        if(not self.isFeasibleToUnassignBusFromService(bId, sId)):
            if(self.verbose): print('Unable to unassign bus(%s) from service(%s)' % (str(bId), str(sId)))
            return(False)
        if(not self.isFeasibleToUnassignDriverFromService(dId, sId)):
            if(self.verbose): print('Unable to unassign driver(%s) from service(%s)' % (str(dId), str(sId)))
            return(False)
        self.busIdtoServiceID[bId].remove(sId)
        if (bId in self.busIdtoServiceID):
            if (len(self.busIdtoServiceID[bId])==0):
                self.numUsedBuses -= 1
                del self.busIdtoServiceID[bId]
        self.driverIdtoServiceID[dId].remove(sId)

        del self.serviceIdtoBusIDDriverId[sId]
      
        self.updateCost()
        return(True)
  
    def getCost(self):
        return(self.cost)
    
    def findFeasibleAssignments(self, sId):
        startEvalTime = time.time()
        evaluatedCandidates = 0
        feasibleAssignments = []

        for bus in self.buses:
            bId = bus.getId()
            for driver in self.drivers:
                dId = driver.getId()
                feasible = self.assign(sId, bId, dId)
                evaluatedCandidates += 1
                if(not feasible): continue
                assignment = Assignment(sId, bId, dId, self.getCost())
                feasibleAssignments.append(assignment)

                self.unassign(sId, bId, dId)

        elapsedEvalTime = time.time() - startEvalTime
        return(feasibleAssignments, elapsedEvalTime, evaluatedCandidates)

    def findBestFeasibleAssignment(self, sId):
        bestAssignment = Assignment(sId, None, None, float('infinity'))
        for bus in self.buses:
            bId = bus.getId()
            for driver in self.drivers:
                dId = driver.getId()
                feasible = self.assign(sId, bId, dId)
                if(not feasible): continue
                curCost = self.getCost()
                if(bestAssignment.cost > curCost):
                    bestAssignment.busId = bId
                    bestAssignment.driverId = dId
                    bestAssignment.cost = curCost
                
                self.unassign(sId, bId, dId)

        return(bestAssignment, 0 ,0)
    
    def __str__(self):  # toString equivalent
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
        
        strSolution = 'z = %10.8f;\n' % self.cost
        
        # Xds: decision variable containing the assignment of driver to services
        # pre-fill with no assignments (all-zeros)
        xds = []
        for d in range(0, nDrivers):   # h = 0..(nDrivers-1)
            xdsEntry = [0] * nServices     # results in a vector of 0's with nServices elements
            xds.append(xdsEntry)

        # iterate over hash table driverIdtoServiceID and fill in xds
        for dId in self.driverIdtoServiceID.keys():
            for sId in self.driverIdtoServiceID[dId]:
                xds[dId][sId] = 1

        strSolution += 'xds = [\n'
        for xdsEntry in xds:
            strSolution += '\t[ '
            for xdsValue in xdsEntry:
                strSolution += str(xdsValue) + ' '
            strSolution += ']\n'
        strSolution += '];\n'
        
        # Xbs: decision variable containing the assignment of bus to services
        # pre-fill with no assignments (all-zeros)
        xbs = []
        for b in range(0, nBuses):     # t = 0..(nBuses-1)
            xbsEntry = [0] * nServices      # results in a vector of 0's with nServices elements
            xbs.append(xbsEntry)
        
        # iterate over hash table busIdtoServiceID and fill in xbs
        for bId in self.busIdtoServiceID.keys():

            for sId in self.busIdtoServiceID[bId]:

                xbs[bId][sId] = 1
        
        strSolution += 'xbs = [\n'
        for xbsEntry in xbs:
            strSolution += '\t[ '
            for xbsValue in xbsEntry:
                strSolution += str(xbsValue) + ' '
            strSolution += ']\n'
        strSolution += '];\n'
        
        return(strSolution)

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()

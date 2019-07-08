'''
AMMM PROJECT
Local Search algorithm.
Copyright 2018 Elena Molina & Miguel Álvarez
Based on: AMMM Lab Heuristics v1.2 Copyright 2018 Luis Velasco.
'''

import copy, time

# A change in a solution in the form: move serviceId from curBusId to newBusId, curDriverId to newDriverId
# This class is used to carry sets of modifications.
# A new solution can be created based on an existing solution and a list of
# changes can be created using the createNeighborSolution(solution, changes) function.
class Change(object):
    def __init__(self, serviceId, curBusId, newBusId, curDriverId, newDriverId):
        self.serviceId = serviceId
        self.curBusId = curBusId
        self.newBusId = newBusId
        self.curDriverId = curDriverId
        self.newDriverId = newDriverId

# Implementation of a local search using two neighborhoods and two different policies.
class LocalSearch(object):
    def __init__(self, config):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy

        self.elapsedTime = 0
        self.iterations = 0

    def createNeighborSolution(self, solution, changes):
        # unassign the services specified in changes
        # and reassign them to the new bus and driver

        newSolution = copy.deepcopy(solution)

        for change in changes:
            newSolution.unassign(change.serviceId, change.curBusId, change.curDriverId)

        for change in changes:
            feasible = newSolution.assign(change.serviceId, change.newBusId, change.newDriverId)
            if(not feasible): return(None)

        return(newSolution)


    def evaluateNeighbor(self, solution, changes):
        availMinPerDriver = [0] * len(solution.drivers)
        doneMinPerBus = [0] * len(solution.buses)
        doneKmPerBus = [0] * len(solution.buses)

        for driver in solution.drivers:
            driverId = driver.getId()
            availMinPerDriver[driverId]=solution.drivers[driverId].getMaxMin()
            for serv in solution.driverIdtoServiceID[driverId]:
                availMinPerDriver[driverId]-=solution.services[serv].getMin()
        for bus in solution.buses:
            busId = bus.getId()
            doneMinPerBus[busId]=0
            doneKmPerBus[busId]=0
            if (busId in solution.busIdtoServiceID):
                for serv in solution.busIdtoServiceID[busId]:
                    doneMinPerBus[busId] +=solution.services[serv].getMin()	
                    doneKmPerBus[busId] += solution.services[serv].getKm()
        for change in changes:
            sId = change.serviceId
            service = solution.services[sId]

            curDriverId = change.curDriverId
            if (curDriverId in solution.driverIdtoServiceID):
                for serv in solution.driverIdtoServiceID[curDriverId]:
                    if (solution.services[serv].getId()!= sId):
                        availMinPerDriver[curDriverId]-=solution.services[serv].getMin()

            curBusId = change.curBusId
            if (curBusId in solution.busIdtoServiceID):
                for serv in solution.busIdtoServiceID[curBusId]:
                    if (solution.services[serv].getId()== sId):
                        doneMinPerBus[curBusId] -=solution.services[serv].getMin()	
                        doneKmPerBus[curBusId] -= solution.services[serv].getKm()	
       

        for change in changes:
            sId = change.serviceId
            service = solution.services[sId]

            newDriverId = change.newDriverId
            driver = solution.drivers[newDriverId]

            driverAvailMin=availMinPerDriver[newDriverId]
            serviceReqMin=service.getMin()
            serviceReqKm=service.getKm()
            selectedDriverId = None

            if (driverAvailMin > serviceReqMin):
                selectedDriverId = newDriverId

            if (selectedDriverId is None):
                return(float('infinity'))

            newBusId = change.newBusId
            selectedBusId = None

            if ( newBusId not in solution.busIdtoServiceID.keys()):
                if (solution.numUsedBuses+1<=solution.maxBuses):
                    selectedBusId=newBusId
            else:
                selectedBusId=newBusId

            if (selectedBusId is None):
                return(float('infinity'))
            availMinPerDriver[selectedDriverId] -= serviceReqMin
            doneMinPerBus[selectedBusId] += serviceReqMin
            doneKmPerBus[selectedBusId] += serviceReqKm

        cost = 0.0
        driverCost = 0.0
        busCost = 0.0
        driverWorkedTime = 0.0
        busWorkedTime = 0.0 
        busWorkedKm = 0.0
        for driver in solution.drivers:
            driverId = driver.getId()
            driverWorkedTime = solution.drivers[driverId].getMaxMin()-availMinPerDriver[driverId]
            if (driverWorkedTime > solution.BM): # worked extra min
                driverCost+=solution.BM*solution.CBM+(driverWorkedTime-solution.BM)*solution.CEM

            else:
                driverCost+=driverWorkedTime*solution.CBM

        for bus in solution.buses:
            bId = bus.getId()
            busWorkedTime = doneMinPerBus[bId]
            busWorkedKm = doneKmPerBus[bId]
            busCost+=busWorkedTime*bus.getBusCPM()+busWorkedKm*bus.getBusCPKm()

        cost = max(cost,(driverCost+busCost))
        return(cost)
    
    def getAssignmentsSortedByCost(self, solution):
        services = solution.getServices()
        buses = solution.getBuses()
        drivers = solution.getDrivers()
        
        # create vector of service assignments.
        # Each element is a tuple <service, [bus,driver]> 
        assignments = []
        for service in services:
            sId = service.getId()
            bId = solution.getBusAssignedToService(sId)
            dId = solution.getDriverAssignedToService(sId)
            bus = buses[bId]
            driver = drivers[dId]
            cost = 0
            driverWorkedTime = 0.0
            if (dId in solution.driverIdtoServiceID):
                for serv in solution.driverIdtoServiceID[dId]:
                    driverWorkedTime+=solution.services[serv].getMin()
                if (driverWorkedTime > solution.BM): # worked extra min
                    cost+=solution.BM*solution.CBM+(driverWorkedTime-solution.BM)*solution.CEM
                else:
                    cost+=driverWorkedTime*solution.CBM
            if (bId in solution.busIdtoServiceID):
                for serv in solution.busIdtoServiceID[bId]:
                    cost+=solution.services[serv].getMin()*bus.getBusCPM()+solution.services[serv].getKm()*bus.getBusCPKm()

            assignment = (service, bus, driver, cost)
            assignments.append(assignment)

        # For best improvement policy it does not make sense to sort the services since all of them must be explored.
        # However, for first improvement, we can start by the services assigned with higher cost.
        if(self.policy == 'BestImprovement'): return(assignments)
        
        # Sort services assignments by the cost in descending order.
        sorted_assignments = sorted(assignments, key=lambda assignment:assignment[3], reverse=True)
        return(sorted_assignments)
    
    def exploreNeighborhood(self, solution):
        services = solution.getServices()
        buses = solution.getBuses()
        drivers = solution.getDrivers()

        curCost = solution.getCost()
        bestNeighbor = solution
        
        if(self.nhStrategy == 'Reassignment'):
            sortedAssignments = self.getAssignmentsSortedByCost(solution)
            for assignment in sortedAssignments:
                service = assignment[0]
                serviceId = service.getId()
                
                curBus = assignment[1]
                curBusId = curBus.getId()

                curDriver = assignment[2]
                curDriverId = curDriver.getId() 

                for bus in buses:
                    newBusId = bus.getId()
                    if(newBusId == curBusId): continue

                    changes = []
                    changes.append(Change(serviceId, curBusId, newBusId, curDriverId, curDriverId))
                    neighborCost = self.evaluateNeighbor(solution, changes)

                    if(curCost > neighborCost):
                        neighbor = self.createNeighborSolution(solution, changes)
                        if(neighbor is None): continue
                        if(self.policy == 'FirstImprovement'):
                            return(neighbor)
                        else:
                            bestNeighbor = neighbor
                            curCost = neighborCost
                for driver in drivers:
                    newDriverId = driver.getId()
                    if(newDriverId == curDriverId): continue

                    changes = []
                    changes.append(Change(serviceId, curBusId, curBusId, curDriverId, newDriverId))
                    neighborCost = self.evaluateNeighbor(solution, changes)

                    if(curCost > neighborCost):
                        neighbor = self.createNeighborSolution(solution, changes)
                        if(neighbor is None): continue
                        if(self.policy == 'FirstImprovement'):
                            return(neighbor)
                        else:
                            bestNeighbor = neighbor
                            curCost = neighborCost                            
        elif(self.nhStrategy == 'Exchange'):
            
            
            sortedAssignments = self.getAssignmentsSortedByCost(solution)
            numAssignments = len(sortedAssignments)
            
            for i in range(0, numAssignments):             # i = 0..(numAssignments-1)
                assignment1 = sortedAssignments[i]
                service1 = assignment1[0]
                serviceId1 = service1.getId()
                
                curBus1 = assignment1[1]
                curBusId1 = curBus1.getId()

                curDriver1 = assignment1[2]
                curDriverId1 = curDriver1.getId()
                for j in range(numAssignments-1, -1, -1):  # j = (numAssignments-1)..0
                    if(i >= j): continue # avoid duplicate explorations and exchange with itself. 
                    assignment2 = sortedAssignments[j]

                    service2 = assignment2[0]
                    serviceId2 = service2.getId()
                    
                    curBus2 = assignment2[1]
                    curBusId2 = curBus2.getId()

                    curDriver2 = assignment2[2]
                    curDriverId2 = curDriver2.getId()
                    # avoid exploring pairs of services assigned to the same bus,drintinue
                    changes = []
                    if (curBusId1 == curBusId2):
                        changes.append(Change(serviceId1, curBusId1, curBusId1, curDriverId1, curDriverId2))
                        changes.append(Change(serviceId2, curBusId1, curBusId1, curDriverId2, curDriverId1))
                    elif (curDriverId1 == curDriverId2):
                        changes.append(Change(serviceId1, curBusId1, curBusId2, curDriverId1, curDriverId1))
                        changes.append(Change(serviceId2, curBusId2, curBusId1, curDriverId1, curDriverId1))
                    else:
                        changes.append(Change(serviceId1, curBusId1, curBusId2, curDriverId1, curDriverId1))
                        changes.append(Change(serviceId2, curBusId2, curBusId1, curDriverId1, curDriverId1))
                        changes.append(Change(serviceId1, curBusId1, curBusId1, curDriverId1, curDriverId2))
                        changes.append(Change(serviceId2, curBusId1, curBusId1, curDriverId2, curDriverId1))
                        changes.append(Change(serviceId1, curBusId1, curBusId2, curDriverId1, curDriverId2))
                        changes.append(Change(serviceId2, curBusId2, curBusId1, curDriverId2, curDriverId1))

                    neighborCost = self.evaluateNeighbor(solution, changes)

                    if(curCost > neighborCost):

                        neighbor = self.createNeighborSolution(solution, changes)

                        if(neighbor is None): continue
                        if(self.policy == 'FirstImprovement'):
                            return(neighbor)
                        else:
                            bestNeighbor = neighbor
                            curCost = neighborCost

        else:
            raise Exception('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)
        
        return(bestNeighbor)
    
    def run(self, solution):
        if(not self.enabled): return(solution)
        if(not solution.isFeasible()): return(solution)
        bestSolution = solution
        bestCost = bestSolution.getCost()
        
        startEvalTime = time.time()
        iterations = 0
        
        # keep iterating while improvements are found
        keepIterating = True
        while(keepIterating):
            keepIterating = False
            iterations += 1
            
            neighbor = self.exploreNeighborhood(bestSolution)
            curCost = neighbor.getCost()
            if(bestCost > curCost):
                bestSolution = neighbor
                bestCost = curCost
                keepIterating = True
        
        self.iterations += iterations
        self.elapsedTime += time.time() - startEvalTime
        
        return(bestSolution)
    
    def printPerformance(self):
        if(not self.enabled): return
        
        avg_evalTimePerIteration = 0.0
        if(self.iterations != 0):
            avg_evalTimePerIteration = 1000.0 * self.elapsedTime / float(self.iterations)
        
        print ('')
        print ('Local Search Performance:')
        print ('  Num. Iterations Eval.', self.iterations)
        print ('  Total Eval. Time     ', self.elapsedTime, 's')
        print ('  Avg. Time / Iteration', avg_evalTimePerIteration, 'ms')

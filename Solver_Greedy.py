'''
AMMM PROJECT
Greedy solver.
Copyright 2018 Elena Molina & Miguel Álvarez
Based on: AMMM Lab Heuristics v1.2 Copyright 2018 Luis Velasco.
'''

from Solver import Solver
from Solution import Solution
from LocalSearch import LocalSearch

# Inherits from a parent abstract solver.
class Solver_Greedy(Solver):
    
    def greedyConstruction(self, config, problem):
        # get an empty solution for the problem
        solution = Solution.createEmptySolution(config, problem)

        # get services and sort them by their total required min in descending order
        services = problem.getServices()
        sortedServices = sorted(services, key=lambda service: service.getMin(), reverse=True)

        elapsedEvalTime = 0
        evaluatedCandidates = 0
        
        # for each service taken in sorted order
        for service in sortedServices:
            sId = service.getId()

            feasibleAssignments, service_elapsedEvalTime, service_evaluatedCandidates = solution.findFeasibleAssignments(sId)
            elapsedEvalTime += service_elapsedEvalTime
            evaluatedCandidates += service_evaluatedCandidates

            # choose assignment with minimum cost
            minCost = float('infinity')
            choosenAssignment = None

            for feasibleAssignment in feasibleAssignments:
                if (feasibleAssignment.cost < minCost):
                    minCost = feasibleAssignment.cost
                    choosenAssignment = feasibleAssignment

            if(choosenAssignment is None):
                solution.makeInfeasible()
                break

            # assign the current service to the bus and driver with min cost 
            solution.assign(service.getId(), choosenAssignment.busId, choosenAssignment.driverId)

        return(solution, elapsedEvalTime, evaluatedCandidates)

    def solve(self, config, problem):
        self.startTimeMeasure()

        self.writeLogLine(float('infinity'), 0)
        
        solution, elapsedEvalTime, evaluatedCandidates = self.greedyConstruction(config, problem)
        self.writeLogLine(solution.getCost(), 1)


        localSearch = LocalSearch(config)
        solution = localSearch.run(solution)

        self.writeLogLine(solution.getCost(), 1)
        
        avg_evalTimePerCandidate = 0.0
        if (evaluatedCandidates != 0):
            avg_evalTimePerCandidate = 1000.0 * elapsedEvalTime / float(evaluatedCandidates)

        print ('')
        print ('Greedy Candidate Evaluation Performance:')
        print ('  Num. Candidates Eval.', evaluatedCandidates)
        print ('  Total Eval. Time     ', elapsedEvalTime, 's')
        print ('  Avg. Time / Candidate', avg_evalTimePerCandidate, 'ms')
        
        localSearch.printPerformance()
        
        return(solution)

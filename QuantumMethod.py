import math

import dimod
from dwave.system import DWaveSampler, EmbeddingComposite, LeapHybridSampler
from dimod import BinaryQuadraticModel
import itertools
import pandas as pd

import TracePlot as TP
import TaskGenerator
import matplotlib.pyplot as plt
import numpy as np
import BruteForceSolution as BFS
import time
import AminKNeuronMethod as ak
import QuantumMethod as QM



class QuantumMethod:
    def __init__(self,taskList, robotList, use_quantum_solver=False):
        self.taskList = taskList
        self.robotList = robotList
        self.m = len(taskList) # num of tasks
        self.k = len(robotList) # num of robots
        self.sampleset = None
        self.minDistance = 0

        # Assign name to each of the task and robots
        tasks = [_ for _ in range(len(taskList))]
        robots = [_ for _ in range(len(robotList))]

        self.tasks = tasks
        self.robots = robots

        # Calculate the distance between each of the task and the distance
        distance = []
        for rx, ry in robotList:
            d = []
            for tx, ty in taskList:
                d.append((rx - tx) ** 2 + (ry - ty) ** 2)
            distance.append(d)
        # print(distance)

        # Step-1, build a variable list for each of the robots
        x = []
        for r in range(len(robots)):
            temp_x = []
            for t in range(len(tasks)):
                temp_x.append(f'R{str(r)}_T{str(t)}')
            x.append(temp_x)

        # Step-2, Initialize BOM
        bqm = BinaryQuadraticModel('BINARY')

        # Step-3, Write the Objective Function
        for r in robots:
            for t in tasks:
                distance_name = x[r][t]
                distance_value = distance[r][t]
                # print(f'The dist {distance_name} is {distance_value}')
                bqm.add_variable(distance_name, distance_value)  # add_variable( x<str>, cost<float>

        # Constraint-1: Every robot only assign to one target
        for r in robots:
            c1 = [(x[r][t], 1) for t in tasks]
            # print(c1)
            bqm.add_linear_equality_constraint(terms=c1, lagrange_multiplier=50, constant=-1)

        # Constraint-2: Every task only assign to one robot
        for t in tasks:
            c2 = [(x[r][t],1) for r in robots]
            bqm.add_linear_equality_constraint(terms=c2, lagrange_multiplier=50, constant=-1)


        # send to solver
        if not use_quantum_solver:
            sampler = dimod.ExactSolver()
            sampleset = sampler.sample(bqm)
            # df = sampleset.to_pandas_dataframe()
            # pd.options.display.max_columns = None
            # df = df.sort_values('energy')
            # print(df.head())
            # print(sampleset.lowest())
        else:
            # sampler = EmbeddingComposite(DWaveSampler())  # this is the pure quantum solver
            # sampleset = sampler.sample(bqm, num_reads=250)
            sampler = LeapHybridSampler() # this is the hybrid solver
            # https://docs.ocean.dwavesys.com/en/stable/docs_system/reference/generated/dwave.system.samplers.LeapHybridSampler.sample.html
            sampleset = sampler.sample(bqm)
            # print(sampleset.first)
        print("initial done")
        self.sampleset = sampleset

    def GenerateRobotPath(self):
        sampleset = self.sampleset
        # print out the arrangement of the lowest energy state
        low_energy_result = sampleset.first.sample # this is a dict

        print("This is the best solution found by Quantum Computer")
        print(sampleset.first.sample)
        arrangement = {} # Robot -> Task

        for r in self.robots:
            for t in self.tasks:
                key = f'R{r}_T{t}'
                if low_energy_result[key]==1:
                    arrangement[r] = t
                    break
        print(arrangement)

        RobotTrace = []
        minDistance = 0

        for i in self.robots:
            trace = [self.robotList[i],self.taskList[arrangement[i]]]
            RobotTrace.append(trace)
            rx, ry = self.robotList[i]
            tx, ty = self.taskList[arrangement[i]]
            d = math.sqrt((rx-tx)**2+(ry-ty)**2)
            minDistance+=d

        self.minDistance = minDistance
        print(f"the total travel distance for Quantum Computer is {minDistance}")
        return RobotTrace





if __name__ == '__main__':
    print("Unit Test")

    valrange = 10  # size of the board
    num_of_robots = 33  # num of the tasks
    num_of_task = num_of_robots

    tasklist = TaskGenerator.GenerateTask(valrange, num_of_task)
    robotList = TaskGenerator.GenerateRobot(valrange, num_of_robots)
    print(tasklist)
    print(robotList)

    f = plt.figure(num=1, figsize=(15, 10))

    # robotList = [[1.61, 7.41], [7.48, 2.89], [1.84, 0.41]]
    # tasklist = [[6.72, 7.39], [0.82, 0.91], [2.56, 6.7]]

    # robotList = [[5.05, 3.11], [5.67, 2.32], [4.4, 0.76], [4.67, 3.49], [1.32, 3.44], [5.01, 2.46], [7.51, 5.27], [3.22, 4.53]]
    # tasklist = [[1.38, 0.74], [1.33, 6.13], [6.96, 6.58], [5.9, 2.4], [3.24, 6.62], [1.24, 7.88], [5.21, 4.85], [5.58, 4.87]]

    # Solution = QuantumMethod(tasklist, robotList, use_quantum_solver= True)
    # print('done')
    # RobotTrace = Solution.GenerateRobotPath()
    # print(RobotTrace)


    ############## Quantum Computer ####################################################
    quantumSolution = QM.QuantumMethod(tasklist, robotList, use_quantum_solver=True)
    quantumRobotTrace = quantumSolution.GenerateRobotPath()
    print(quantumRobotTrace)
    quantumTracePlot = TP.TracePlot(tasklist, quantumRobotTrace, valrange)
    qdist = quantumSolution.minDistance
    quantumTracePlot.getRobotTracyPlot(f, 1, 1, 1, "Travel Distance for Quantum is " + str(np.round(qdist, 2)))

    plt.show()


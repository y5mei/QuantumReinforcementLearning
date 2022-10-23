# This is a test runner that I will compare the NN solver with the quantum solver
# Dec 25, 2021.
import TracePlot as TP
import TaskGenerator
import matplotlib.pyplot as plt
import numpy as np
import BruteForceSolution as BFS
import time
import AminKNeuronMethod as ak
import QuantumMethod as QM

valrange = 10 # size of the board
num_of_robots = 10 # num of the tasks
num_of_task = num_of_robots

############################## This is the Brute Froce Method ############################
# tasklist = TaskGenerator.GenerateTask(valrange,num_of_task)
tasklist = [[1.38, 0.74], [1.33, 6.13], [6.96, 6.58], [5.9, 2.4], [3.24, 6.62], [1.24, 7.88], [5.21, 4.85], [5.58, 4.87]]
# tasklist = [[6.72, 7.39], [0.82, 0.91], [2.56, 6.7]]
# tasklist = [[1.63, 4.59], [4.59, 5.29], [4.5, 1.58], [2.22, 3.3], [4.15, 4.59], [0.13, 0.01], [3.74, 2.18]]
print("The task list is:")
print(tasklist)
# robotList = TaskGenerator.GenerateRobot(valrange,num_of_robots)
robotList = [[5.05, 3.11], [5.67, 2.32], [4.4, 0.76], [4.67, 3.49], [1.32, 3.44], [5.01, 2.46], [7.51, 5.27], [3.22, 4.53]]
# robotList = [[1.61, 7.41], [7.48, 2.89], [1.84, 0.41]]
# robotList = [[1.75, 0.23], [4.12, 5.83], [4.02, 6.09], [1.3, 3.21], [0.11, 2.34], [2.74, 0.11], [3.25, 5.45]]
print("The robot position list is:")
print(robotList)
# Count the Running time of BruteForce Method
# start_time = time.time()
# Solution = BFS.BruteForceSolution(tasklist,robotList)
# print("--- brute force method time: %10f seconds ---" % (time.time() - start_time))

# Make the plots
# RobotTrace = Solution.GenerateRobotPath()
# TracePlot = TP.TracePlot(tasklist, RobotTrace,valrange)

# Create a Figure Object, and assign this object to each of the method that can create a subplot
# This is the only way how we can merge subplots into one Figure
# Each of the methods need to return the Figure object!!!
f = plt.figure(num=1, figsize=(15,10))
# TracePlot.getRobotTracyPlot(f,1,4,4, "Brute force min Travel Dist is "+str(Solution.minDistance))
# test = Solution.getDistanceHistogram(f,1,4,3)

# plt.savefig('220.png')
# plt.show()

############################## Amin's easier method with K output ############################
# Amin's easier method
# newtasklist = TaskGenerator.GenerateTask(valrange,5)
# newrobotlist = TaskGenerator.GenerateRobot(valrange,8)
# print(newrobotlist)
newSolution = ak.AminKNeuronMethod(tasklist,robotList)
start_time = time.time()
newstep = newSolution.generateRobotPathWhenKequalM()
print("--- K neurons method time: %10f seconds ---" % (time.time() - start_time))
print ("============The task assigned list is", newSolution.taskAssigned2)
print(newstep)
nndist = newSolution.calculateTravelDistance()
print("the total travel distance for NN is", nndist)
aaa = TP.TracePlot(tasklist,newstep, valrange)
aaa.getRobotTracyPlot(f,1,4,2, "Travel Distance for NN is "+str(np.round(nndist,2)))
aaa.getRobotTracyPlot(f,1,4,1, "Travel Distance for NN is "+str(np.round(nndist,2)))

############## Quantum Computer ####################################################
quantumSolution = QM.QuantumMethod(tasklist,robotList,use_quantum_solver=True)
quantumRobotTrace = quantumSolution.GenerateRobotPath()
print("=============!!!================")
print(quantumRobotTrace)
quantumTracePlot = TP.TracePlot(tasklist, quantumRobotTrace,valrange)
qdist = quantumSolution.minDistance
quantumTracePlot.getRobotTracyPlot(f,1,4,3, "Travel Distance for Quantum is "+str(np.round(qdist,2)))

# This is the only way to get a subplot out of a Figure Object!!
allaxes = f.get_axes()
# This is to add a line in a subplot and annotation
allaxes[1].axvline(np.round(nndist,2), color='r', linestyle='dashed', linewidth=5)
allaxes[1].text(nndist*1.1, allaxes[1].get_ylim()[1]*0.9, 'NN Solution: {:.2f}'.format(nndist),color='r', size=20)
plt.show()